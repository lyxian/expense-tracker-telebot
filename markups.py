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
            *[InlineKeyboardButton(text=val, callback_data=f"date:{current.month}-{val}-{current.year}") if val else InlineKeyboardButton(text="-", callback_data=" ") for val in row]
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

def createMarkupPrice(digits=''):
    # Options
    markup = InlineKeyboardMarkup(row_width=3)
    nums = [str(i) for i in range(1,10)]
    if '.' not in digits:
        dot = digits + '.'
    else:
        dot = 'INVALID'
    if digits[-1] == ' ':
        clear = 'IGNORE'
        enter = 'IGNORE'
        dot = digits + '0.'
    else:
        clear = 'DEL {}'
        enter = 'ENTER {}'
    # Add Inline
    markup.add(
        *[InlineKeyboardButton(text=num, callback_data=digits+num) for num in nums[:3]]
    )
    markup.add(
        *[InlineKeyboardButton(text=num, callback_data=digits+num) for num in nums[3:6]]
    )
    markup.add(
        *[InlineKeyboardButton(text=num, callback_data=digits+num) for num in nums[6:]]
    )
    markup.add(
        InlineKeyboardButton(text='.', callback_data=dot),
        InlineKeyboardButton(text='0', callback_data=digits+'0'),
        InlineKeyboardButton(text="C", callback_data=clear.format(digits))
    )
    markup.add(
        InlineKeyboardButton(text="Enter", callback_data=enter.format(digits))
    )
    return markup