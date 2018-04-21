# -*- coding: utf-8 -*-
import redis
import os
import telebot
import math
import random
import threading
import info
import test
from telebot import types
from emoji import emojize
token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)

games={}


@bot.message_handler(commands=['startgame'])
def startgame(m):
    if m.chat.id not in games:
        games.update(creategame(m.chat.id))
        Keyboard=types.InlineKeyboardMarkup()
        Keyboard.add(types.InlineKeyboardButton(text='Join', url='telegram.me/crossfirebot?start='+str(m.from_user.id)))
        bot.send_message(m.chat.id, 'telegram.me/crossfirebot?start='+str(m.from_user.id), reply_markup=Keyboard)
    else:
        bot.send_message(m.chat.id, 'Игра уже запущена! Жмите "присоединиться"!')
    
   

def creategame(id):
    return {id:{
        'players':{}
    }
           }
        




if __name__ == '__main__':
  bot.polling(none_stop=True)



