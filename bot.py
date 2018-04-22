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


def medit(message_text,chat_id, message_id,reply_markup=None,parse_mode='Markdown'):
    return bot.edit_message_text(chat_id=chat_id,message_id=message_id,text=message_text,reply_markup=reply_markup,
                                 parse_mode=parse_mode)


@bot.message_handler(commands=['start'])
def start(m):
    x=m.text.split('/start')
    if len(x)==2:
       try:
        if m.from_user.id not in games[int(x[1])]['players']:
          if int(x[1])<0:
            i=0
            for ids in games[int(x[1])]['players']:
                i+=1
            if len(games[int(x[1])]['players'])<=2:
                games[int(x[1])]['players'].update(createuser(m.from_user.id, m.from_user.first_name, i+1))
                for ids in games[int(x[1])]['players']:
                    if games[int(x[1])]['players'][ids]['id']==m.from_user.id:
                        player=games[int(x[1])]['players'][ids]
                bot.send_message(m.from_user.id, 'Вы успешно присоединились!')
                bot.send_message(games[int(x[1])]['id'], player['name']+' присоединился!')
       except:
        if m.chat.id==m.from_user.id:
            bot.send_message(m.from_user.id, 'Игра crossfire')

@bot.message_handler(commands=['startgame'])
def startgame(m):
  if m.chat.id<0:
    if m.chat.id not in games:
        t=threading.Timer(300, begin, args=[m.chat.id])
        t.start()
        games.update(creategame(m.chat.id, t))   
        Keyboard=types.InlineKeyboardMarkup()
        Keyboard.add(types.InlineKeyboardButton(text='Join', url='telegram.me/crossfirebot?start='+str(m.chat.id)))
        bot.send_message(m.chat.id, 'Присоединиться', reply_markup=Keyboard)
    else:
        Keyboard=types.InlineKeyboardMarkup()
        Keyboard.add(types.InlineKeyboardButton(text='Join', url='telegram.me/crossfirebot?start='+str(m.chat.id)))
        bot.send_message(m.chat.id, 'Игра уже запущена! Жмите "присоединиться"!', reply_markup=Keyboard)
  else:
    bot.send_message(m.chat.id, 'Играть можно только в группах!')
    
   
def begin(id):
    if len(games[id]['players'])>=2:
        bot.send_message(id, 'Игра начинается!')
        try:
            games[id]['timer'].cancel()
        except:
            pass
        xod(games[id])
    else:
        bot.send_message(id, 'Недостаточно игроков!')
        try:
            del games[id]
        except:
            pass

        
@bot.message_handler(commands=['forcestart'])
def forcem(m):
  if m.chat.id in games:
    i=0
    x=bot.get_chat_administrators(m.chat.id)
    for z in x:       
        if m.from_user.id==z.user.id:
           i=1
        else:
            if i!=1:
                i=10
    if i==1:
        if m.chat.id in games:
            begin(m.chat.id)
    else:
        bot.send_message(m.chat.id, 'Только администратор может использовать эту команду!')
        
        

def xod(game):
    if len(game['players'])==2:
        roless=['glavar','killer']
    elif len(game['players'])==3:
        roless=['agent','killer', 'glavar']
    elif len(game['players'])==4:
        roless=['agent','killer', 'glavar', 'prohojii']
    elif len(game['players'])==5:
        roless=['agent','killer', 'glavar', 'prohojii', 'primanka']
    elif len(game['players'])==6:
        roless=['agent','killer', 'glavar', 'prohojii', 'primanka','mirotvorets']
    elif len(game['players'])==7:
        roless=['agent','killer', 'glavar', 'prohojii', 'primanka','agent', 'killer']
    elif len(game['players'])==8:
        roless=['glavar', 'prohojii', 'podrivnik','gangster','killer', 'killer', 'telohranitel','redprimanka']
    pick=[]
    for g in game['players']:
        x=random.randint(0, len(game['players'])-1)
        while x in pick:
            x=random.randint(0, len(game['players'])-1)
        game['players'][g]['role']=roless[x]
        pick.append(x)
        print(game)
    for g in game['players']:
        if game['players'][g]['role']=='agent':
            text='Ты агент'
        elif game['players'][g]['role']=='killer':
            text='Ты киллер'
        elif game['players'][g]['role']=='prohojii':
            text='Ты прохожий'
        elif game['players'][g]['role']=='primanka':
            text='Ты приманка'
        elif game['players'][g]['role']=='glavar':
            text='Ты главарь'
        elif game['players'][g]['role']=='telohranitel':
            text='Ты телохранитель'
        bot.send_message(game['players'][g]['id'], text)
    players=[]
    text=''
    for g in game['players']:
        players.append(game['players'][g]['name'])
    for gg in players:
        text+=gg+'\n'
    bot.send_message(game['id'], 'Игроки: \n'+'*'+text+'*', parse_mode='markdown')
    t=threading.Timer(5, shuffle1, args=[game])
    t.start()
            
 
def shuffle1(game):
    roles=[]
    for ids in game['players']:
        roles.append(game['players'][ids]['role'])
    i=0
    for ids in game['players']:
        try:
            game['players'][ids]['role']=roles[i+1]
            i+=1
        except:
            game['players'][ids]['role']=roles[0]
    bot.send_message(game['id'], 'Ваши роли были переданы человеку над вами! Теперь посмотрите свои новые роли.')
    for g in game['players']:
        if game['players'][g]['role']=='agent':
            text='Ты агент'
        elif game['players'][g]['role']=='killer':
            text='Ты киллер'
        elif game['players'][g]['role']=='prohojii':
            text='Ты прохожий'
        elif game['players'][g]['role']=='primanka':
            text='Ты приманка'
        elif game['players'][g]['role']=='glavar':
            text='Ты главарь'
        elif game['players'][g]['role']=='telohranitel':
            text='Ты телохранитель'
        bot.send_message(game['players'][g]['id'], text)
    t=threading.Timer(5, shuffle2, args=[game])
    t.start()
        
    
                     

def shuffle2(game):
    roles=[]
    for ids in game['players']:
        roles.append(game['players'][ids]['role'])
    first=random.randint(1, len(game['players']))
    shuffles=len(game['players'])/3
    if shuffles<1:
        shuffles=1
    i=0
    centers=[]
    while i<shuffles:
        for ids in game['players']:
            if game['players'][ids]['number']==first:
                mid=game['players'][ids]
                centers.append(mid['name'])
            if first+1<=len(game['players']):
                if game['players'][ids]['number']==first+1:
                    bottom=game['players'][ids]
            else:
                if game['players'][ids]['number']==1:
                    bottom=game['players'][ids]
            if first-1>=1:                
                if game['players'][ids]['number']==first-1:
                    top=game['players'][ids]
            else:
                if game['players'][ids]['number']==len(game['players']):
                    top=game['players'][ids]              
        users=[]
        roles=[]
        users.append(mid)
        users.append(bottom)
        users.append(top)
        roles.append(bottom['role'])
        roles.append(mid['role'])
        roles.append(top['role'])
        pick=[]
        for g in users:
            x=random.randint(0, 2)
            while x in pick:
                x=random.randint(0, 2)
            g['role']=roles[x]
            pick.append(x)
        if first==len(game['players']):
            first=2
        elif first==len(game['players'])-1:
            first=1
        else:
            first+=2
        i+=1
    text2=''
    for ids in centers:
        text2+=ids+'\n'
    bot.send_message(game['id'], 'Ваши роли были перемешаны по 3 штуки! Центры перемешивания: *\n'+text2+'*', parse_mode='markdown')
    for g in game['players']:
        if game['players'][g]['role']=='agent':
            game['players'][g]['cankill']=1
            game['players'][g]['blue']=1
            text='Ты агент'
        elif game['players'][g]['role']=='killer':
            game['players'][g]['cankill']=1
            game['players'][g]['red']=1
            text='Ты киллер'
        elif game['players'][g]['role']=='prohojii':
            game['players'][g]['cankill']=0
            text='Ты прохожий'
        elif game['players'][g]['role']=='primanka':
            game['players'][g]['cankill']=0
            text='Ты приманка'
        elif game['players'][g]['role']=='glavar':
            game['players'][g]['cankill']=0
            text='Ты главарь'
            game['players'][g]['blue']=1
        elif game['players'][g]['role']=='telohranitel':
            game['players'][g]['candef']=1
            text='Ты телохранитель'
            game['players'][g]['blue']=1
        bot.send_message(game['players'][g]['id'], text)
    t=threading.Timer(30, shoot, args=[game])
    t.start()
      



def shoot(game):
    for g in game['players']:
        Keyboard=types.InlineKeyboardMarkup()
        for ids in game['players']:
            if game['players'][ids]['id']!=game['players'][g]['id']:
                Keyboard.add(types.InlineKeyboardButton(text=game['players'][ids]['name'], callback_data=str(game['players'][ids]['number'])))
        bot.send_message(game['players'][g]['id'], 'Кого ты выбираешь целью?', reply_markup=Keyboard)
    t=threading.Timer(30, endshoot, args=[game])
    t.start()
        

        
@bot.callback_query_handler(func=lambda call:True)
def inline(call):
    x=0
    for ids in games:
        if call.from_user.id in games[ids]['players']: 
            game=games[ids]
            x=1
    if x==1:
            for z in game['players']:
                if game['players'][z]['number']==int(call.data):
                    target=game['players'][z]
            game['players'][call.from_user.id]['text']=game['players'][call.from_user.id]['name']+' стреляет в '+target['name']
            medit('Выбор сделан: '+target['name'],call.from_user.id,call.message.message_id)
            game['players'][call.from_user.id]['target']=target
            
        

def endshoot(game):
    text=''
    for ids in game['players']:
        if game['players'][ids]['text']!=None:
            text+=game['players'][ids]['text']+'\n'
        else:
            text+=game['players'][ids]['name']+' не стреляет\n'
    bot.send_message(game['id'], text)
    t=threading.Timer(10, reallyshoot, args=[game])
    t.start()
        

def reallyshoot(game):
    for ids in game['players']:
        game['players'][ids]['text']=''
        if game['players'][ids]['candef']==1:
            if game['players'][ids]['target']!=None:
                game['players'][ids]['target']['defence']=1
                game['players'][ids]['text']+=game['players'][ids]['name']+' Защищает '+game['players'][ids]['target']['name']+'!'
                
    for ids in game['players']:
        if game['players'][ids]['blue']==1:
            if game['players'][ids]['target']!=None:
                if game['players'][ids]['cankill']==1:
                    if game['players'][ids]['target']['defence']!=1:
                        game['players'][ids]['target']['killed']=1
                        game['players'][ids]['killany']=game['players'][ids]['target']          
                    else:
                        game['players'][ids]['killany']=None
                    game['players'][ids]['text']+=game['players'][ids]['name']+' стреляет в '+game['players'][ids]['target']['name']+'!'
                
    for ids in game['players']:
        if game['players'][ids]['target']!=None:
          if game['players'][ids]['red']==1:
            if game['players'][ids]['cankill']==1:
                if game['players'][ids]['target']['defence']!=1:
                    game['players'][ids]['target']['killed']=1
                    game['players'][ids]['killany']=game['players'][ids]['target']          
                else:
                    game['players'][ids]['killany']=None
                game['players'][ids]['text']+=game['players'][ids]['name']+' стреляет в '+game['players'][ids]['target']['name']+'!'
    text=''
    for ids in game['players']:
        text+=game['players'][ids]['text']+'\n'
    bot.send_message(game['id'],'По-настоящему выстрельнувшие:\n'+text)
    text=''
    live=emojize(':neutral_face:', use_aliases=True)
    dead=emojize(':skull:', use_aliases=True)
    blue=emojize(':large_blue_circle:', use_aliases=True)
    red=emojize(':red_circle:', use_aliases=True)
    yellow=emojize(':full_moon:', use_aliases=True)
    pobeda=emojize(':thumbsup:', use_aliases=True)
    porajenie=emojize(':-1:', use_aliases=True)
    for ids in game['players']:
        if game['players'][ids]['blue']==1:
            color=blue
        elif game['players'][ids]['red']==1:
            color=red
        else:
            color=yellow
        if game['players'][ids]['role']=='agent':
            role='Агент'
        elif game['players'][ids]['role']=='killer':
            role='Киллер'
        elif game['players'][ids]['role']=='prohojii':
            role='Прохожий'
        elif game['players'][ids]['role']=='primanka':
            role='Приманка'
        elif game['players'][ids]['role']=='glavar':
            role='Главарь'
        elif game['players'][ids]['role']=='telohranitel':
            role='Телохранитель'
        if game['players'][ids]['killed']==1:
            alive=dead+'Мёртв'
        else:
            alive=live+'Жив'
        for idss in game['players']:
            if game['players'][idss]['role']=='glavar':
                glavar=game['players'][idss]
        if game['players'][ids]['blue']==1:
            if glavar['killed']==0:
                win=pobeda+'Выиграл\n'
            else:
                win=porajenie+'Проиграл\n'
            if game['players'][ids]['killany']['role']=='prohojii':
                win=porajenie+'Проиграл (убил прохожего)\n'
            if game['players'][ids]['killany']['role']=='primanka':
                win=porajenie+'Проиграл (убил приманку)\n'
        elif game['players'][ids]['red']==1:
            if glavar['killed']==1:
                win=pobeda+'Выиграл\n'
            else:
                win=porajenie+'Проиграл\n'
            if game['players'][ids]['killany']['role']=='prohojii':
                    win=porajenie+'Проиграл (убил прохожего)\n'
            if game['players'][ids]['killany']['role']=='primanka':
                    win=porajenie+'Проиграл (убил приманку)\n'
        elif game['players'][ids]['yellow']==1:
            if game['players'][ids]['role']=='prohojii':
                if game['players'][ids]['killed']==1:
                    win=porajenie+'Проиграл\n'
                else:
                    win=pobeda+'Выиграл\n'
                if game['players'][ids]['role']=='primanka':
                    if game['players'][ids]['killed']==1:
                        win=pobeda+'Выиграл\n'
                    else:
                        win=porajenie+'Проиграл\n'
        text+=game['players'][ids]['name']+': '+color+role+','+alive+','+win
    bot.send_message(game['id'], 'Результаты игры:\n'+text)
    del games[game['id']]
        
        
def creategame(id, t):
    return {id:{
        'players':{},
        'id':id,
        'timer':t
    }
           }
        

def createuser(id, name, x):
    return{id:{
        'role':None,
        'name':name,
        'id':id,
        'number':x,
        'text':None,
        'shuffle':0,
        'target':None,
        'killed':0,
        'cankill':0,
        'defence':0,
        'killany':None,
        'candef':0,
        'blue':0,
        'red':0,
        'win':0
    }
          }
    
                      
                      
                      



if __name__ == '__main__':
  bot.polling(none_stop=True)



