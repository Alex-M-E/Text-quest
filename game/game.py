import json
import random as rd
import time
from pygame import mixer 
# одкулючаем библиотеки

# фигачим музон
mixer.init()
mixer.music.load('music/dobro-pojalovat-na-server-shizofreniya-original.mp3')
mixer.music.play()

# устанвливаем состояние звука
sound = True

# окрываем файл с игрой
with open('game.json', encoding='windows-1251') as f:
    data = json.load(f)

print(data['ruels']) # выводим правила
a = data['level'] # устанавливаем уровень
game = True # не нужная переменная
ff = {} # словарь с ключами с переходами
for i in range(len(data[a]['togo'])):
    ff[str(i)] = data[a]['togo'][i] # заполняем словарь
# цыкл игры
while game:
    # выводим текст
    print(data[a]["text"])
    if 'kill' in data[a]: # провека на изменения (разбирайтесь сами что это значит)
        d = data['kill' + data[a]['kill']]
        for i in d:
            exec(i) # выполняем команды
    if 'music' in data[a]: # проверка на музон
        if sound is True:
            # хреначим музон
            mixer.init()
            mixer.music.load('music/' + data[a]['music'])
            mixer.music.play()
    if 'luck' in data[a]: # проверка на удачу (хз что это)
        a = data[a]['luck'][rd.randint(0, len(data[a]["luck"])) - 1] # преходим на новый уровень
        continue
    if data[a]["togo"] == []: # проверка на конец игры
        print(data[a]["st"])
        print('Начать занова - /start')
        c = input()
        # проверяем хочет ли игрок продолжить игру
        if c == '/start':
            # если да то обнулянем прохождение
            with open('game.json', encoding='windows-1251') as f:
                data = json.load(f)
            a = data['level']
            continue
        else:
            # если нет то конец
            break
    ff = {} # пустой словарь для преходов
    for i in range(len(data[a]['togo'])):
        ff[str(i)] = data[a]['togo'][i] # заполняем переходами
    # пустая строка
    b = ""
    # хреначим пока не игрок не введт что то дельное
    while b not in ff:
        b = input()
        # выходи
        if b == '/exit':
            game = False
            b = a
            break
        # все занова (опять)
        elif b == '/start':
            with open('game.json', encoding='windows-1251') as f:
                data = json.load(f)
            f = {}
            ff[b] = data['level'] 
            break
        # настройки звука
        elif b == '/setting':
            if sound is True:
                print('sound - on')
                print('off? +: да, -: нет')
                c = input()
                while c != '+' and a != '-':
                    print("Что-то не то")
                    c = input()
                if c == '+':
                    sound = False 
            else:
                print('sound - off')
                print('on? +: да, -: нет')
                c = input()
                while c != '+' and a != '-':
                    print("Что-то не то")
                    c = input()
                if c == '+':
                    sound = True
            continue
        # сохраняем файл как
        elif b == '/save':
            c = input()
            with open(c + '.json', 'w') as file:
                json.dump(data, file, ensure_ascii=False)
            continue
        # открфываем файл как
        elif b == '/open':
            c = input()
            with open(c + '.json') as file:
                data = json.load(file)
                ff = {}
                ff[b] = data['level']
            break
        # выводим правила
        elif b == '/rule':
            print(data['ruels'])
        # пользователь ввел хрень
        elif b not in ff:
            print('Что?')
        else:
            pass # как ты сюда попал
    data['level'] = ff[b]
    a = ff[b]
# сохранение прохождения
print('Сохранить (просто введите /save, если хотите сохранит, а далее название файла)')
a = input()
if a == '/save':
    c = input()
    with open(c + '.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False)
