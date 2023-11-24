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

from markups import createMarkupCalendar, createMarkupCategory
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

    validCallbacks = ['date', 'category']
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
        if int(db.outputLast):
            text = 'You have already joined expense-tracker!'
        else:
            db.runInsert('users', {
                'username': message.chat.username,
                'id': message.chat.id
            })
            text = 'You have successfully joined expense-tracker!'
        bot.send_message(message.chat.id, text)
        return
    
    def checkValidCallback(callback):
        return callback.data[0] == '/' or callback.data.split(':')[0] in validCallbacks

    @bot.callback_query_handler(func=lambda callback: checkValidCallback(callback))
    def _callback(callback):
        currentCommand = callback.data.split(':')[0]
        currentValues = dict([i.split(':') for i in callback.data.split(',')])

        if currentCommand == '/cancel':
            bot.send_message(chat_id=callback.message.chat.id, text='cancel')
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
            bot.edit_message_text(
                text='{} @ {}\nHow much was it?'.format(currentValues['category'], currentValues['date']),
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
            )
        return

    @bot.message_handler(commands=['add'])
    def _add(message):
        # bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        bot.send_message(message.chat.id, 'Choose Date', reply_markup=createMarkupCalendar())

    return bot