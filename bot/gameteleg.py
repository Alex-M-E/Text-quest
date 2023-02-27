import telebot
from telebot import types
import json
import random as rd
import time

with open('gamet.json', encoding='windows-1251') as f:
    data = json.load(f)
a = data['level']
ff = {}
for i in range(len(data[a]['togo'])):
    ff['/' + str(i)] = data[a]['togo'][i]

bot = telebot.TeleBot('secret token')

@bot.message_handler(commands=["start"])
def start(m, res=False):
    global a
    global data
    global ff
    if m.text == "/start":
        print('Кто-то начал игру')
        with open('gamet.json', encoding='windows-1251') as f:
            data = json.load(f)
            a = data['level']
            ff = {}
            for i in range(len(data[a]['togo'])):
                ff['/' + str(i)] = data[a]['togo'][i]
        bot.send_message(m.from_user.id, data[a]['text'])
        for i in ff:
            bot.send_message(m.from_user.id, i + " - " + data[a][ff[i]])
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("/start")
    item2=types.KeyboardButton("/rule")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(m.from_user.id, 'Выберай пункт',  reply_markup=markup)
      
    
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global a
    global data
    global ff
    if message.text == '/rule':
        bot.send_message(message.from_user.id, data['ruels'])
    elif message.text in ff:
        a = ff[message.text]
        bot.send_message(message.from_user.id, data[a]['text'])
        if 'kill' in data[a]:
            d = data['kill' + data[a]['kill']]
            for i in d:
                exec(i)
        if 'luck' in data[a]:
            a = data[a]['luck'][rd.randint(0, len(data[a]["luck"])) - 1]
            if data[a]['togo'] == []:
                bot.send_message(message.from_user.id, data[a]['text'])
                bot.send_message(message.from_user.id, data[a]['st'])
                print('Пользователь закончил игру')
                return None
        elif data[a]['togo'] == []:
            bot.send_message(message.from_user.id, data[a]['st'])
            print('Пользователь закончил игру')
        ff = {}
        for i in range(len(data[a]['togo'])):
            ff['/' + str(i)] = data[a]['togo'][i]
        for i in ff:
            bot.send_message(message.from_user.id, i + " - " + data[a][ff[i]])
        return None     
    else:
        bot.send_message(message.from_user.id, "Чо?")
bot.polling(none_stop=True, interval=0)
