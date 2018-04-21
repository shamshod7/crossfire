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


@bot.send_message(commands=['start'])
def start(m):
    x=m.text.split('/start')
    if len(x)==2:
        if x[0]>0 and x[1]<0:
            if x[0]==m.from_user.id:
                games[x[1]]['players'].update(createuser(m.from_user.id, m.from_user.first_name))
                bot.send_message(m.from_user.id, 'Вы успешно присоединились!')

@bot.message_handler(commands=['startgame'])
def startgame(m):
    if m.chat.id not in games:
        games.update(creategame(m.chat.id))
        Keyboard=types.InlineKeyboardMarkup()
        Keyboard.add(types.InlineKeyboardButton(text='Join', url='telegram.me/crossfirebot?start='+m.from_user.id+' '+m.chat.id))
        bot.send_message(m.chat.id, 'Присоединиться', reply_markup=Keyboard)
    else:
        bot.send_message(m.chat.id, 'Игра уже запущена! Жмите "присоединиться"!')
    
   

def creategame(id):
    return {id:{
        'players':{}
    }
           }
        

def createuser(id, name):
    return{'id':{
        'role':None,
        'name':name
    }
          }
    
                      
                      
                      



if __name__ == '__main__':
  bot.polling(none_stop=True)



