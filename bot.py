from cryptography.fernet import Fernet
import traceback
import requests
import logging
import telebot
import time
import re
import os

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
import subprocess
import pendulum

from markups import createMarkupCalendar, createMarkupCategory, createMarkupConfirm, statusMap, categoryMap
from utils import getToken
from db import DB


def callTelegramAPI(method, params):
    url = 'https://api.telegram.org/bot{}/{}'.format(getToken(), method)
    response = requests.post(url=url, params=params)
    print(response.json())
    return response

def createBot():
    db = DB(dbName='test', logFile='tmp.log')
    TOKEN = getToken()
    bot = telebot.TeleBot(token=TOKEN)
    # bot.checkAuth = False
    # bot.isAuthorized = False
    # bot.awaitingInput = False

    validCallbacks = ['date', 'category', 'confirm']
    # markup = ReplyKeyboardMarkup(row_width=len(buttons))
    # markup.add(*[KeyboardButton(button) for button in buttons])

    @bot.message_handler(commands=['start', 'help'])
    def _start(message):
        text = [
            "Welcome to expense-tracker-bot! Here's a list of commands to get started:",
            '/help - show this message',
            '/join - register user in DB',
            '/add - add new expense record',
            '/query - <TBD>',
        ]
        bot.send_message(message.chat.id, '\n'.join(text))
        return

    @bot.message_handler(commands=['join'])
    def _join(message):
        # query user in users
        db.runSelect('users', column='count(id)', condition=f'id = "{message.chat.id}"')
        output = db.outputLast
        if int(output):
            text = 'You have already joined expense-tracker!'
        else:
            db.runInsert('users', {
                'username': message.chat.username,
                'id': message.chat.id
            })
            text = 'You have successfully joined expense-tracker!'
        bot.send_message(message.chat.id, text)
        return

    @bot.message_handler(commands=['add'])
    def _add(message):
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        db.runSelect('users', column='id, username', condition=f'id = "{message.chat.id}"', showColumn=True)
        d = DB._resultToJson(db.outputLast)
        if message.chat.id in d:
            bot.send_message(message.chat.id, 'Choose Date', reply_markup=createMarkupCalendar())
        else:
            bot.send_message(message.chat.id, 'You have not joined expense-tracker, please do /join first')
        return
    
    def checkValidCallback(callback):
        return callback.data[0] == '/' or callback.data.split(':')[0] in validCallbacks

    @bot.callback_query_handler(func=checkValidCallback) 
    def _callback(callback):
        currentCommand = callback.data.split(':')[0]
        if ':' in callback.data:
            currentValues = dict([i.split(':') for i in callback.data.split(',')])

        if currentCommand == '/cancel':
            bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        elif currentCommand == '/date':
            n = eval(currentValues['/date'])
            bot.edit_message_text(
                text=f'Choose Date',
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                reply_markup=createMarkupCalendar(n)
            )
        elif currentCommand == 'date':
            bot.edit_message_text(
                text=f'Choose Category @ {currentValues["date"]}',
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                reply_markup=createMarkupCategory(callback.data)
            )
        elif currentCommand == 'category':
            messsage = '{} @ {}'.format(currentValues['category'], currentValues['date'])
            # insert/update last callback id
            db.runInsertUpdate('messages', {
                'id': callback.message.chat.id,
                'status': statusMap['awaitAmount'],
                'message': '{}'.format(messsage),
                'lastCallbackId': callback.message.message_id,
            }, 'status = {}, lastCallbackId = {}, message = "{}"'.format(statusMap['awaitAmount'], callback.message.message_id, messsage))
            bot.edit_message_text(
                text='{}\nHow much was it?'.format(messsage),
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
            )
        elif currentCommand == 'confirm':
            if currentValues['confirm'] == 'yes':
                print(currentValues) 
                # insert new record
                db.runInsert('records', {
                    'id': callback.message.chat.id,
                    'category': categoryMap[currentValues['category']],
                    'amount': currentValues['amount'],
                    # 'comment': '',
                    'timestamp': currentValues['date']
                })
                bot.edit_message_text(
                    text="New record created at {}".format(pendulum.now(tz='Asia/Singapore').to_datetime_string()),
                    chat_id=callback.message.chat.id,
                    message_id=callback.message.message_id,
                ) 
            else:
                bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        return

    def awaitAmount(message):
        db.runSelect('messages', column='id, lastCallbackId, statuses.status', joinType='LEFT JOIN', joinTable='statuses', joinOn=('status', 'num'), showColumn=True)
        d = DB._resultToJson(db.outputLast)
        return message.chat.id in d and d[message.chat.id]['status'] == 'awaitAmount'
        
    @bot.message_handler(func=awaitAmount)
    def _awaitAmount(message):
        db.runSelect('messages', column='id, lastCallbackId, statuses.status', joinType='LEFT JOIN', joinTable='statuses', joinOn=('status', 'num'), showColumn=True)
        d = DB._resultToJson(db.outputLast)
        
        db.runSelect('messages', column='message', condition=f'id = "{message.chat.id}"')
        output = db.outputLast
        markupData = ','.join([':'.join(i) for i in zip(['category', 'date', 'amount'], f'{output} @ {message.text}'.split(' @ '))])

        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        bot.edit_message_text(
            text='{}\n${} -- Please confirm'.format(output, message.text),
            chat_id=message.chat.id,
            message_id=d[message.chat.id]['lastCallbackId'],
            reply_markup=createMarkupConfirm(markupData)
        )

        # insert/update last callback id
        db.runInsertUpdate('messages', {
            'id': message.chat.id,
            'status': statusMap['awaitConfirm'],
            'message': '{} @ ${}'.format(output, message.text),
            'lastCallbackId': d[message.chat.id]['lastCallbackId'],
        }, 'status = {}'.format(statusMap['awaitConfirm']))

    @bot.message_handler(commands=['test'])
    def _test(message):
        # bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        db.runSelect('messages', column='message', condition=f'id = "{message.chat.id}"')
        currMessage = db.outputLast
        print(currMessage)

    return bot