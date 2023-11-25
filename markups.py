from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
import pendulum
import calendar

CATEGORIES = [
    'dining',
    'shopping',
    'transport',
    'entertainment',
    'miscellaneous',
]

WEEKDAYS = [
    'Mon',
    'Tue',
    'Wed',
    'Thu',
    'Fri',
    'Sat',
    'Sun'
]

statusMap = {
    'awaitAmount': 1,
    'awaitComment': 2,
    'awaitConfirm': 3,
    'done': 4
}

categoryMap = {
    'dining': 1,
    'shopping': 2,
    'transport': 3,
    'entertainment': 4,
    'miscellaneous': 5
}


class CalendarObject():

    def __init__(self, now):
        self.year = now.year
        self.month = now.month
        self.monthName = calendar.month_name[now.month]
        self.days = calendar.monthcalendar(now.year, now.month)

def createMarkupCalendar(n=0):
    current = CalendarObject(pendulum.now().add(months=n))

    markup = InlineKeyboardMarkup(row_width=7)
    # Add Month
    markup.add(
        InlineKeyboardButton(text=f'{current.monthName}-{current.year}', callback_data=" ")
    )
    # Add Weekdays
    markup.add(
        *[InlineKeyboardButton(text=day, callback_data=" ") for day in WEEKDAYS]
    )
    # Add Days
    for row in current.days:
        markup.add(
            *[InlineKeyboardButton(text=val, callback_data=f"date:{current.year}-{current.month}-{val}") if val else InlineKeyboardButton(text="-", callback_data=" ") for val in row]
        )
    # Commands
    markup.add(
        InlineKeyboardButton("Back", callback_data=f"/date:{n}-1"),
        InlineKeyboardButton("Cancel", callback_data="/cancel"),
        InlineKeyboardButton("Next", callback_data=f"/date:{n}+1")
    )
    return markup

def createMarkupCategory(data):
    markup = InlineKeyboardMarkup(row_width=3)
    # Add First Row
    markup.add(
        *[InlineKeyboardButton(text=category, callback_data=f'category:{category},{data}') for category in CATEGORIES[:3]]
    )
    # Add Second Row
    markup.add(
        *[InlineKeyboardButton(text=category, callback_data=f'category:{category},{data}') for category in CATEGORIES[3:]]
    )
    return markup

def createMarkupConfirm(data):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        *[InlineKeyboardButton(text=response, callback_data=f'confirm:{response},{data}') for response in ['yes', 'no']]
    )
    return markup