import pandas
from sqlalchemy import create_engine
import random
import telebot
from telebot import types
from sqlalchemy.orm import sessionmaker

df= pandas.read_csv('jokes.csv')
jokes=df['text'].tolist()
engine=create_engine('sqlite:///jokes.db')
Session = sessionmaker(bind=engine)
session = Session()
bot = telebot.TeleBot('7928628883:AAFZDd29ABNVnls-lyZlPeemhNdWSBRJj9Y')

@bot.message_handler(commands=['start'])
def start(msg):
    if f'{msg.from_user.last_name}'=='None':
        mess = f'Привет, <b>{msg.from_user.first_name}</b>, если ты напишешь /anekdot, то я скину тебе рандомный анекдот'
    else:
        mess = f'Привет, <b>{msg.from_user.first_name} {msg.from_user.last_name}</b>, если ты напишешь /anekdot, то я скину тебе рандомный анекдот'
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button = types.KeyboardButton('/anekdot')
    keyboard.add(button)
    bot.send_message(msg.chat.id, mess, parse_mode='html', reply_markup=keyboard)


@bot.message_handler(commands=['anekdot'])
def get_text(msg):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button = types.KeyboardButton('/anekdot')
    keyboard.add(button)
    bot.send_message(msg.chat.id, random.choice(jokes), parse_mode='html', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_text(msg):
    try:
        print(msg.from_user.username, msg.text)
        x=msg.text.lower()
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        button = types.KeyboardButton('/anekdot')
        keyboard.add(button)
        if x in ['пиздец', 'хуй', 'хуи', 'хуйня', 'залупа', 'пидор', 'хуета', 'говно', 'дерьмо', 'параша', 'ссанина', 'лох', 'артем', 'артём', 'бля', 'блядь', 'блять', 'ебать', 'пизда']:
            bot.send_message(msg.chat.id, f'сам ты {x}', parse_mode='html', reply_markup=keyboard)
        else:
            img = open('beer.gif', 'rb')
            bot.send_video(msg.chat.id, img, None, 'Text', reply_markup=keyboard)
            img.close()
    except TimeoutError:
        bot.send_message(msg.chat.id, f'{msg.from_user.first_name}, полегче а то взорвусь', parse_mode='html', reply_markup=keyboard)

bot.polling(none_stop=True)

