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


@bot.message_handler(commands=['start'])
def start(m):
    x=m.text.split('/start')
    if len(x)==2:
       try:
        if m.from_user.id not in games[int(x[1])]['players']:
          if int(x[1])<0:
            games[int(x[1])]['players'].update(createuser(m.from_user.id, m.from_user.first_name))
            bot.send_message(m.from_user.id, 'Вы успешно присоединились!')
       except:
        if m.chat.id==m.from_user.id:
            bot.send_message(m.from_user.id, 'Игра crossfire')

@bot.message_handler(commands=['startgame'])
def startgame(m):
    if m.chat.id not in games:
        t=threading.Timer(20, begin, args=[m.chat.id])
        games.update(creategame(m.chat.id))
        Keyboard=types.InlineKeyboardMarkup()
        Keyboard.add(types.InlineKeyboardButton(text='Join', url='telegram.me/crossfirebot?start='+str(m.chat.id)))
        bot.send_message(m.chat.id, 'Присоединиться', reply_markup=Keyboard)
    else:
        bot.send_message(m.chat.id, 'Игра уже запущена! Жмите "присоединиться"!')
    
   
def begin(id):
    if len(games[id]['players'])>1:
        bot.send_message(id, 'Игра начинается!')
    else:
        bot.send_message(id, 'Недостаточно игроков!')
        games[id].del()



def creategame(id):
    return {id:{
        'players':{}
    }
           }
        

def createuser(id, name):
    return{id:{
        'role':None,
        'name':name
    }
          }
    
                      
                      
                      



if __name__ == '__main__':
  bot.polling(none_stop=True)



