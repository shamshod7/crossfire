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
from pymongo import MongoClient
token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)

games={}

client1=os.environ['database']
client=MongoClient(client1)
db=client.god
user=db.users
token=db.tokens
mob=db.mobs


def medit(message_text,chat_id, message_id,reply_markup=None,parse_mode='Markdown'):
    return bot.edit_message_text(chat_id=chat_id,message_id=message_id,text=message_text,reply_markup=reply_markup,
                                 parse_mode=parse_mode)


if True:
    user.remove({})


@bot.message_handler(commands=['start'])
def start(m):
    x=user.find_one({'id':m.from_user.id})
    if x==None:
        user.insert_one({'id':m.from_user.id,
                         'name':m.from_user.first_name,
                         'win':0,
                         'loose':0,
                         'games':0,
                         'red':0,
                         'blue':0,
                         'yellow':0,
                         'agent':0,
                         'killer':0,
                         'glavar':0,
                         'prohojii':0,
                         'primanka':0,
                         'mirotvorets':0,
                         'gangster':0,
                         'podrivnik':0,
                         'redprimanka':0,
                         'telohranitel':0,
                         'alive':0
                        })
        print('Юзер создал аккаунт! Его имя: '+m.from_user.first_name)
    x=m.text.split('/start')
    if len(x)==2:
       try:
        if m.from_user.id not in games[int(x[1])]['players']:
         if len(games[int(x[1])]['players'])<10:
          if int(x[1])<0:
            i=0
            for ids in games[int(x[1])]['players']:
                i+=1         
            if games[int(x[1])]['play']==0:
                games[int(x[1])]['players'].update(createuser(m.from_user.id, m.from_user.first_name, i+1))
                for ids in games[int(x[1])]['players']:
                    if games[int(x[1])]['players'][ids]['id']==m.from_user.id:
                        player=games[int(x[1])]['players'][ids]
                bot.send_message(m.from_user.id, 'Вы успешно присоединились!')
                bot.send_message(games[int(x[1])]['id'], player['name']+' присоединился!')
         else:
            bot.send_message(m.from_user.id, 'Слишком много игроков! Мест не осталось!')
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
        msg=bot.send_message(m.chat.id, 'Присоединиться', reply_markup=Keyboard)
        for ids in games:
            if games[ids]['id']==m.chat.id:
                game=games[ids]
        game['todel'].append(msg.message_id)
    else:
      if games[m.chat.id]['play']==0:
        Keyboard=types.InlineKeyboardMarkup()
        Keyboard.add(types.InlineKeyboardButton(text='Join', url='telegram.me/crossfirebot?start='+str(m.chat.id)))
        msg=bot.send_message(m.chat.id, 'Игра уже запущена! Жмите "присоединиться"!', reply_markup=Keyboard)
        for ids in games:
            if games[ids]['id']==m.chat.id:
                game=games[ids]
        game['todel'].append(msg.message_id)
  else:
    bot.send_message(m.chat.id, 'Играть можно только в группах!')
    
   
def begin(id):
  if id in games:
   if games[id]['play']==0:
    if len(games[id]['players'])>=5:
        for ids in games[id]['todel']:
            try:
                bot.delete_message(id, ids)
            except:
                pass
       
        bot.send_message(id, 'Игра начинается!')
        try:
            games[id]['timer'].cancel()
        except:
            pass
        games[id]['play']=1
        xod(games[id])
    else:
        for ids in games[id]['todel']:
            bot.delete_message(id, ids)
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
    elif len(game['players'])==9:
        roless=['glavar', 'prohojii', 'podrivnik','agent','killer', 'killer', 'agent','killer', 'agent'] #'loialistblue','povstanetsred'
    elif len(game['players'])==10:
        roless=['glavar', 'prohojii', 'mirotvorets','agent','killer', 'killer', 'agent','killer', 'agent', 'podrivnik'] 
        
    pick=[]
    for g in game['players']:
        x=random.randint(0, len(game['players'])-1)
        while x in pick:
            x=random.randint(0, len(game['players'])-1)
        game['players'][g]['role']=roless[x]
        pick.append(x)
        print(game)
    roletext=[]
    for g in game['players']:
        if game['players'][g]['role']=='agent':
            text='Ты агент'
            roletext.append('Агент')
        elif game['players'][g]['role']=='killer':
            text='Ты киллер'
            roletext.append('Киллер')
        elif game['players'][g]['role']=='prohojii':
            text='Ты прохожий'
            roletext.append('Прохожий')
        elif game['players'][g]['role']=='primanka':
            text='Ты приманка'
            roletext.append('Приманка')
        elif game['players'][g]['role']=='glavar':
            text='Ты главарь'
            roletext.append('Главарь')
        elif game['players'][g]['role']=='telohranitel':
            text='Ты телохранитель'
            roletext.append('Телохранитель')
        elif game['players'][g]['role']=='mirotvorets':
            text='Ты миротворец'
            roletext.append('Миротворец')
        elif game['players'][g]['role']=='podrivnik':
            text='Ты подрывник'
            roletext.append('Подрывник')
        elif game['players'][g]['role']=='gangster':
            text='Ты гангстер'
            roletext.append('Гангстер')
        elif game['players'][g]['role']=='redprimanka':
            text='Ты красная приманка'
            roletext.append('Красная приманка')
            
        bot.send_message(game['players'][g]['id'], text)
    players=[]
    roletext1=[]
    numbers=[]
    roletextfinal=''
    while len(roletext1)<len(roletext):
        i=random.randint(0, len(roletext)-1)
        if i not in numbers:
            roletext1.append(roletext[i])
            numbers.append(i)
    for bb in roletext1:
        roletextfinal+=bb+'\n'     
    text=''
    for g in game['players']:
        players.append(game['players'][g]['name'])
    for gg in players:
        text+=gg+'\n'
    bot.send_message(game['id'], 'Роли: \n*'+roletextfinal+'*', parse_mode='markdown')
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
        elif game['players'][g]['role']=='podrivnik':
            text='Ты подрывник'
        elif game['players'][g]['role']=='mirotvorets':
            text='Ты миротворец'
        elif game['players'][g]['role']=='gangster':
            text='Ты гангстер'
        elif game['players'][g]['role']=='redprimanka':
            text='Ты красная приманка'
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
            game['players'][g]['yellow']=1
            text='Ты прохожий'
        elif game['players'][g]['role']=='primanka':
            game['players'][g]['cankill']=0
            game['players'][g]['yellow']=1
            text='Ты приманка'
        elif game['players'][g]['role']=='glavar':
            game['players'][g]['cankill']=0
            text='Ты главарь'
            game['players'][g]['blue']=1
        elif game['players'][g]['role']=='telohranitel':
            game['players'][g]['candef']=1
            text='Ты телохранитель'
            game['players'][g]['blue']=1
        elif game['players'][g]['role']=='podrivnik':
            game['players'][g]['cankill']=0
            text='Ты подрывник'
            game['players'][g]['yellow']=1
        elif game['players'][g]['role']=='mirotvorets':
            game['players'][g]['candef']=1
            text='Ты миротворец'
            game['players'][g]['yellow']=1
        elif game['players'][g]['role']=='gangster':
            text='Ты гангстер'
            game['players'][g]['blue']=1
            game['players'][g]['cankill']=1
        elif game['players'][g]['role']=='redprimanka':
            text='Ты красная приманка'
            game['players'][g]['red']=1
        bot.send_message(game['players'][g]['id'], text)
    t=threading.Timer(240, shoot, args=[game])
    t.start()
      



def shoot(game):
    for g in game['players']:
        Keyboard=types.InlineKeyboardMarkup()
        for ids in game['players']:
            if game['players'][ids]['id']!=game['players'][g]['id']:
                Keyboard.add(types.InlineKeyboardButton(text=game['players'][ids]['name'], callback_data=str(game['players'][ids]['number'])))
        msg=bot.send_message(game['players'][g]['id'], 'Кого ты выбираешь целью?', reply_markup=Keyboard)
        game['players'][g]['message']={'msg':msg,
                                       'edit':1
                                      }
                                       
    bot.send_message(game['id'], 'Теперь выбирайте, на кого хотите направить пистолеты!')
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
            if game['players'][call.from_user.id]['role']!='gangster':
                game['players'][call.from_user.id]['text']='*'+game['players'][call.from_user.id]['name']+'*'+'🔫стреляет в '+target['name']
                medit('Выбор сделан: '+target['name'],call.from_user.id,call.message.message_id)
                game['players'][call.from_user.id]['message']['edit']=0
                game['players'][call.from_user.id]['target']=target
            else:
              if game['players'][call.from_user.id]['picks']>0:
                if game['players'][call.from_user.id]['picks']==2:
                    game['players'][call.from_user.id]['text']+='*'+game['players'][call.from_user.id]['name']+'*'+'🔫стреляет в '+target['name']+'\n'
                else:
                    game['players'][call.from_user.id]['text']+='*'+game['players'][call.from_user.id]['name']+'*'+'🔫стреляет в '+target['name']
                medit('Выбор сделан: '+target['name'],call.from_user.id,call.message.message_id)
                game['players'][call.from_user.id]['message']['edit']=0
                if game['players'][call.from_user.id]['target']==None:
                    game['players'][call.from_user.id]['target']=target
                else:
                    game['players'][call.from_user.id]['target2']=target
                game['players'][call.from_user.id]['picks']-=1
                for g in game['players']:
                    Keyboard=types.InlineKeyboardMarkup()
                    for ids in game['players']:
                        if game['players'][ids]['id']!=game['players'][g]['id'] and game['players'][ids]['id']!=game['players'][g]['target']['id']:
                            Keyboard.add(types.InlineKeyboardButton(text=game['players'][ids]['name'], callback_data=str(game['players'][ids]['number'])))
                msg=bot.send_message(call.from_user.id, 'Теперь выберите вторую цель')
                game['players'][call.from_user.id]['message']={'msg':msg,
                                       'edit':1
                                      }
              else:
                medit('Выбор сделан: '+target['name'],call.from_user.id,call.message.message_id)
            
        

def endshoot(game):
    text=''
    for msg in game['players']:
        if game['players'][msg]['message']['edit']==1:
            medit('Время вышло!', game['players'][msg]['message']['msg'].chat.id, game['players'][msg]['message']['msg'].message_id)
    for ids in game['players']:
        if game['players'][ids]['text']!='':
            text+=game['players'][ids]['text']+'\n'
        else:
            text+='*'+game['players'][ids]['name']+'*'+'💨не стреляет\n'
    bot.send_message(game['id'], text, parse_mode='markdown')
    t=threading.Timer(8, reallyshoot, args=[game])
    t.start()
        

def reallyshoot(game):
    for ids in game['players']:
        game['players'][ids]['text']=''
        if game['players'][ids]['candef']==1:
            if game['players'][ids]['target']!=None:
                game['players'][ids]['target']['defence']+=1
                game['players'][ids]['text']+='*'+game['players'][ids]['name']+'*'+' Защищает '+game['players'][ids]['target']['name']+'!'
                
    for ids in game['players']:
        if game['players'][ids]['blue']==1:
            if game['players'][ids]['target']!=None:
                if game['players'][ids]['cankill']==1:
                    if game['players'][ids]['target']['defence']<1:
                        game['players'][ids]['target']['killed']=1
                        game['players'][ids]['target']['killedby'].append(game['players'][ids]['role'])
                        game['players'][ids]['target']['golos']=0
                        game['players'][ids]['killany']=game['players'][ids]['target']          
                    else:
                        game['players'][ids]['target']['defence']-=1
                        game['players'][ids]['killany']=None
                    game['players'][ids]['text']+='*'+game['players'][ids]['name']+'*'+'🔫стреляет в '+game['players'][ids]['target']['name']
            if game['players'][ids]['target2']!=None:
                if game['players'][ids]['cankill']==1:
                    if game['players'][ids]['target2']['defence']<1:
                        game['players'][ids]['target2']['killed']=1
                        game['players'][ids]['target']['killedby'].append(game['players'][ids]['role'])
                        game['players'][ids]['target2']['golos']=0
                        game['players'][ids]['killany2']=game['players'][ids]['target2']          
                    else:
                        game['players'][ids]['target2']['defence']-=1
                        game['players'][ids]['killany2']=None
                    game['players'][ids]['text']+='*'+game['players'][ids]['name']+'*'+'🔫стреляет в '+game['players'][ids]['target2']['name']+'!'
                
    for ids in game['players']:
        if game['players'][ids]['target']!=None:
          if game['players'][ids]['red']==1:
            if game['players'][ids]['cankill']==1:
              if game['players'][ids]['golos']==1:
                if game['players'][ids]['target']['defence']<1:
                    game['players'][ids]['target']['killed']=1
                    game['players'][ids]['target']['killedby'].append(game['players'][ids]['role'])
                    game['players'][ids]['killany']=game['players'][ids]['target']          
                else:
                    game['players'][ids]['target']['defence']-=1
                    game['players'][ids]['killany']=None
                game['players'][ids]['text']+='*'+game['players'][ids]['name']+'*'+'🔫стреляет в '+game['players'][ids]['target']['name']+'!'
              else:
                game['players'][ids]['text']+='*'+game['players'][ids]['name']+'*'+'☠️Убит! (не стреляет)'
                
    text=''
    for ids in game['players']:
        text+=game['players'][ids]['text']+'\n'
    bot.send_message(game['id'],'По-настоящему выстрелившие:\n'+text, parse_mode='markdown')
    text=''
    role=game['players'][ids]['role']
    live=emojize(':neutral_face:', use_aliases=True)
    dead=emojize(':skull:', use_aliases=True)
    blue=emojize(':large_blue_circle:', use_aliases=True)
    red=emojize(':red_circle:', use_aliases=True)
    yellow=emojize(':full_moon:', use_aliases=True)
    pobeda=emojize(':thumbsup:', use_aliases=True)
    porajenie=emojize(':-1:', use_aliases=True)
    podrivnik=0
    for podriv in game['players']:
        if game['players'][podriv]['role']=='podrivnik':
            if game['players'][podriv]['killed']==0:
                podrivnik=1
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
        elif game['players'][ids]['role']=='mirotvorets':
            role='Миротворец'
        elif game['players'][ids]['role']=='gangster':
            role='Гангстер'
        elif game['players'][ids]['role']=='podrivnik':
            role='Подрывник'
        elif game['players'][ids]['role']=='redprimanka':
            role='Красная приманка'
        if game['players'][ids]['killed']==1:
            alive=dead+'Мёртв'
        else:
            alive=live+'Жив'
        for idss in game['players']:
            if game['players'][idss]['role']=='glavar':
                glavar=game['players'][idss]
        if game['players'][ids]['blue']==1:
            if glavar['killed']==0:
              if podrivnik!=1:
                win=pobeda+'Выиграл\n'
              else:
                win=porajenie+'Проиграл\n'
            else:
                win=porajenie+'Проиграл\n'
            if game['players'][ids]['killany']!=None:
                if game['players'][ids]['killany']['role']=='prohojii':
                    win=porajenie+'Проиграл (убил прохожего)\n'
                if game['players'][ids]['killany2']!=None:
                    if game['players'][ids]['killany2']['role']=='prohojii':
                        win=porajenie+'Проиграл (убил прохожего)\n'
                if game['players'][ids]['killany2']!=None:
                    if game['players'][ids]['killany']['role']=='primanka':
                        win=porajenie+'Проиграл (убил приманку)\n'
                if game['players'][ids]['killany2']!=None:
                    if game['players'][ids]['killany2']['role']=='primanka':
                        win=porajenie+'Проиграл (убил приманку)\n'
        elif game['players'][ids]['red']==1:
          if game['players'][ids]['role']!='redprimanka':
            if glavar['killed']==1:
              if podrivnik!=1:
                win=pobeda+'Выиграл\n'
              else:
                win=porajenie+'Проиграл\n'
            else:
                win=porajenie+'Проиграл\n'
            if game['players'][ids]['killany']!=None:
                if game['players'][ids]['killany']['role']=='prohojii':
                        win=porajenie+'Проиграл (убил прохожего)\n'
                if game['players'][ids]['killany']['role']=='primanka':
                        win=porajenie+'Проиграл (убил приманку)\n'
          else:            
            if glavar['killed']==1 or game['players'][ids]['killed']==1:
              if podrivnik!=1:
                win=pobeda+'Выиграл\n'
              else:
                win=porajenie+'Проиграл\n'
            else:
                win=porajenie+'Проиграл\n'
            if 'gangster' or 'agent' in game['players'][ids]['killedby']:
                if podrivnik!=1:
                    win=pobeda+'Выиграл\n'
                else:
                    win=porajenie+'Проиграл\n'
        elif game['players'][ids]['yellow']==1:
            if game['players'][ids]['role']=='prohojii':
                if game['players'][ids]['killed']==1:
                    win=porajenie+'Проиграл\n'
                else:
                  if podrivnik!=1:
                    win=pobeda+'Выиграл\n'
                  else:
                    win=porajenie+'Проиграл\n'
            if game['players'][ids]['role']=='primanka':
                    if game['players'][ids]['killed']==1:
                      if podrivnik!=1:
                        win=pobeda+'Выиграл\n'
                      else:
                        win=porajenie+'Проиграл\n'
                    else:
                        win=porajenie+'Проиграл\n'
            if game['players'][ids]['role']=='mirotvorets':
                    i=0
                    for prohojii in game['players']:
                        if game['players'][prohojii]['role']=='prohojii' and game['players'][prohojii]['killed']==1:
                            i=1
                    if i==1:
                        win=porajenie+'Проиграл\n'
                    else:
                      if podrivnik!=1:
                        win=pobeda+'Выиграл\n'
                      else:
                        win=porajenie+'Проиграл\n'
            if role=='podrivnik':
                if game['players'][ids]['killed']==0:
                    win=pobeda+'Выиграл\n'
                else:
                    win=porajenie+'Проиграл\n'
        text+=game['players'][ids]['name']+': '+color+role+','+alive+','+win
        if color==red:
            user.update_one({'id':game['players'][ids]['id']}, {'$inc':{'red':1}})
        elif color==blue:
            user.update_one({'id':game['players'][ids]['id']}, {'$inc':{'blue':1}})
        elif color==yellow:
            user.update_one({'id':game['players'][ids]['id']}, {'$inc':{'yellow':1}})
        if role=='Агент':
            user.update_one({'id':game['players'][ids]['id']}, {'$inc':{'agent':1}})
        elif role=='Киллер':
            user.update_one({'id':game['players'][ids]['id']}, {'$inc':{'killer':1}})
        elif role=='Прохожий':
            user.update_one({'id':game['players'][ids]['id']}, {'$inc':{'prohojii':1}})
        elif role=='Приманка':
            user.update_one({'id':game['players'][ids]['id']}, {'$inc':{'primanka':1}})
        elif role=='Главарь':
            user.update_one({'id':game['players'][ids]['id']}, {'$inc':{'glavar':1}})
        elif role=='Телохранитель':
            user.update_one({'id':game['players'][ids]['id']}, {'$inc':{'telohranitel':1}})
        elif role=='Миротворец':
            user.update_one({'id':game['players'][ids]['id']}, {'$inc':{'mirotvorets':1}})
        elif role=='Гангстер':
            user.update_one({'id':game['players'][ids]['id']}, {'$inc':{'gangster':1}})
        elif role=='Подрывник':
            user.update_one({'id':game['players'][ids]['id']}, {'$inc':{'podrivnik':1}})
        elif role=='Красная приманка':
            user.update_one({'id':game['players'][ids]['id']}, {'$inc':{'redprimanka':1}})
        if alive==live+'Жив':
            user.update_one({'id':game['players'][ids]['id']}, {'$inc':{'alive':1}})
        if win==pobeda+'Выиграл\n':
            user.update_one({'id':game['players'][ids]['id']}, {'$inc':{'win':1}})
        elif win==porajenie+'Проиграл\n':
            user.update_one({'id':game['players'][ids]['id']}, {'$inc':{'loose':1}})
        user.update_one({'id':game['players'][ids]['id']}, {'$inc':{'games':1}})
            
    bot.send_message(game['id'], 'Результаты игры:\n'+text)
    del games[game['id']]
        
     
        
def creategame(id, t):
    return {id:{
        'players':{},
        'id':id,
        'timer':t,
        'todel':[],
        'toedit':[],
        'play':0
    }
           }
        

def createuser(id, name, x):
    return{id:{
        'role':None,
        'name':name,
        'id':id,
        'number':x,
        'text':'',
        'shuffle':0,
        'target':None,
        'target2':None,
        'killed':0,
        'cankill':0,
        'defence':0,
        'killany':None,
        'killany2':None,
        'candef':0,
        'blue':0,
        'red':0,
        'yellow':0,
        'win':0,
        'golos':1,
        'message':0,
        'picks':2,
        'killedby':[]
    }
          }
    
                      
                      
                      



if __name__ == '__main__':
  bot.polling(none_stop=True)



