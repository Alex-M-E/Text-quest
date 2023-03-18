import telebot
from telebot import types
import json
import random as rd
import time
# библеотеки

# Открываем файл и загружаем стартовый словарь
with open('gamet.json', encoding='windows-1251') as f:
    data = json.load(f)
a = data['level'] # устанавливаем уровень
ff = {} #  словарь для перехода
# наполняем словарь ключами (/0, /1, .. ) к уровням 
for i in range(len(data[a]['togo'])):
    ff['/' + str(i)] = data[a]['togo'][i]

bot = telebot.TeleBot('5890454132:AAG0Ad9szAx3jEdkxV7vJaJo6NJftKnwI0g') # читай документации

# функция для команды старт
@bot.message_handler(commands=["start"])
def start(m, res=False):
    # глобальные переменные а - уровень, data - большой соварь с игрой, ff - словарь для перехода
    global a
    global data
    global ff
    print('Кто-то начал игру') 
    # делаем то же что и на девятой строчке (обнуляем прохождение)
    with open('gamet.json', encoding='windows-1251') as f:
        data = json.load(f)
        a = data['level']
    ff = {}
    for i in range(len(data[a]['togo'])):
        ff['/' + str(i)] = data[a]['togo'][i]
    bot.send_message(m.from_user.id, data[a]['text']) # печатаем текст
    # выводим номера для переходов
    for i in ff:
        bot.send_message(m.from_user.id, i + " - " + data[a][ff[i]])
    # создаем кнопки для команд /start и /rule и для переходов на другие уровни
    make_buttons(m)
    
# функция для вводимых данных   
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # глобльные переменные 
    global a
    global data
    global ff
    # проверка на команду /rule
    if message.text == '/rule':
        bot.send_message(message.from_user.id, data['ruels'])
    # проверка на ключ для перехода
    elif message.text in ff:
        a = ff[message.text] # переходим на уровень
        bot.send_message(message.from_user.id, data[a]['text']) # выводим текс
        # kill - это указатель на те изменения которые нужно провести с data (в конце jsonа можну увидеть команды)
        if 'kill' in data[a]:
            d = data['kill' + data[a]['kill']]
            # перебираем команды
            for i in d:
                exec(i) # исполняем команды
        # luck - исход выбора зависит от удачи
        if 'luck' in data[a]:
            a = data[a]['luck'][rd.randint(0, len(data[a]["luck"])) - 1] # из списка случайным образом выбираем ключ для нового уровня
            # проверка на конец игры
            if data[a]['togo'] == []:
                ff = {}
                bot.send_message(message.from_user.id, data[a]['text'])
                bot.send_message(message.from_user.id, data[a]['st'])
                print('Пользователь закончил игру')
                return None
        # провека на конец игры (зачем мне делать две проверки на одно и тоже, а я ж говно кодер поэтому все норм)
        elif data[a]['togo'] == []:
            bot.send_message(message.from_user.id, data[a]['st'])
            ff = {}
            print('Пользователь закончил игру')
        ff = {}
        for i in range(len(data[a]['togo'])):
            ff['/' + str(i)] = data[a]['togo'][i]
        for i in ff:
            bot.send_message(message.from_user.id, i + " - " + data[a][ff[i]])
        return None     
    # если мы попали сюда значит пользователь ввел хрень
    else:
        bot.send_message(message.from_user.id, "Чо?")

# создаем кнопки      
@bot.message_handler(content_types=['text'])
def make_buttons(m, res=False):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("/start")
    item2=types.KeyboardButton("/rule")
    markup.add(item1)
    markup.add(item2)
    item4=types.KeyboardButton("/0")
    item5=types.KeyboardButton("/1")
    item6=types.KeyboardButton("/2")
    markup.add(item4)
    markup.add(item5)
    markup.add(item6)
    bot.send_message(m.from_user.id, 'Выберай пункт',  reply_markup=markup)
bot.polling(none_stop=True, interval=0) # стора без которой не будет работать
