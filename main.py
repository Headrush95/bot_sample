import telebot
import datetime as dt


class User:
    def __init__(self, name):
        self.name = name
        self.sex = None
        self.age = None


token = ''
bot = telebot.TeleBot(token)

HELP = """
    Доступные команды:
    /help - напечатать справку по доступным командам.
    /name - изменить свое имя в чате.
    /add - добавить задачу в список.
    /show - напечатать задачи на ближайшие два дня.
    /show_all - напечатать все задачи.
    """

schedule = {}
now = dt.datetime.utcnow() + dt.timedelta(hours=3)
today = now.strftime('%d.%m.%Y')
tomorrow = (now + dt.timedelta(days=1)).strftime('%d.%m.%Y')
the_day_after_tommorow = (now + dt.timedelta(days=2)).strftime('%d.%m.%Y')
User.name = 'Unknown user'

@bot.message_handler(content_types=['text'])
def get_message(message):
    return message

@bot.message_handler(commands=['start'])
def init(message):
    bot.send_message(message.chat.id, f'Добро пожаловать в тестовую зону.\nВведите свое имя с помощью команды\n/name')


@bot.message_handler(commands=['help'])
def show_help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['name'])
def set_name(message):
    User.name = message.text.split(maxsplit=1)[1]
    bot.send_message(message.chat.id, f'Здравствуй, {User.name}')


@bot.message_handler(commands=['add'])
def add(message):
    command = message.text.split(maxsplit=2)
    date = command[1]
    task = command[2]
    if date in ['сегодня', 'today']:
        date = today
    elif date in ['завтра', 'tomorrow']:
        date = tomorrow
    elif date in ['послезавтра', 'the day after tomorrow', 'day after tomorrow', 'after tomorrow']:
        date = the_day_after_tommorow
    elif len(date.split('.')) == 3:
        day = date.split('.')[0]
        month = date.split('.')[1]
        year = date.split('.')[2]
        if not (day.isdigit() and month.isdigit() and year.isdigit() and 1 <= int(day) <= 31 and 1 <= int(month) <= 12
                and int(year) > 0):
            bot.send_message(message.chat.id, 'Введите корректную дату в формате д.м.г.')
            return
    else:
        bot.send_message(message.chat.id, 'Введите дату в формате д.м.г.')
        return

    if date not in schedule:
        schedule[date] = []

    schedule[date].append(task)
    bot.send_message(message.chat.id, f'Задача "{task}" добавлена на дату {date}.')


@bot.message_handler(commands=['show'])
def show(message):
    if today in schedule:
        text = 'Задачи на сегодня:' + '\n'
        for task in schedule[today]:
            text += f' - {task}' + '\n'
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, 'Задач на сегодня нет.')

    if tomorrow in schedule:
        text = 'Задачи на завтра:' + '\n'
        for task in schedule[tomorrow]:
            text += f' - {task}' + '\n'
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, 'Задач на завтра нет.')

    if the_day_after_tommorow in schedule:
        text = 'Задачи на послезавтра:' + '\n'
        for task in schedule[the_day_after_tommorow]:
            text += f' - {task}' + '\n'
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, 'Задач на послезавтра нет.')


@bot.message_handler(commands=['show_all'])
def show_all(message):
    if len(schedule) > 0:
        text = ''
        for day in schedule:
            text_day = f'Задачи на {day}:' + '\n'
            for task in schedule[day]:
                text_day += f' - {task}' + '\n'
            text += text_day + '\n' * 2
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, 'Задач нет.')


bot.polling(none_stop=True)
