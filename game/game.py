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
game = True # нужная переменная
ff = {} # словарь с ключами с переходами
for i in range(len(data[a]['togo'])):
    ff[str(i)] = data[a]['togo'][i] # заполняем словарь
    
def kill(a):
    global data
    d = data['kill' + data[a]['kill']]
    for i in d:
        exec(i) # выполняем команды
        
def music(a):
    global data, sound
    if sound is True:
        # хреначим музон
        mixer.init()
        mixer.music.load('music/' + data[a]['music'])
        mixer.music.play()
        
def luck(a):
    global data
    return data[a]['luck'][rd.randint(0, len(data[a]["luck"])) - 1]
        
def setting():
    global sound
    if sound is True:
        print('sound - on')
        print('off? +: да, -: нет')
        c = input()
        while c != '+' and c != '-':
            print("Что-то не то")
            c = input()
        if c == '+':
            sound = False 
    else:
        print('sound - off')
        print('on? +: да, -: нет')
        c = input()
        while c != '+' and c != '-':
            print("Что-то не то")
            c = input()
        if c == '+':
            sound = True
        
def opening():
    global data, ff, b
    c = input()
    with open(c + '.json') as file:
        data = json.load(file)
        ff = {}
        ff[b] = data['level']
        
def start():
    global data, ff, b
    with open('game.json', encoding='windows-1251') as f:
        data = json.load(f)
    ff = {}
    ff[b] = data['level']
    
def save():
    global data
    c = input()
    with open(c + '.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False)
        
def completion_ff():
    global ff, data, a
    ff = {} # пустой словарь для преходов
    for i in range(len(data[a]['togo'])):
        ff[str(i)] = data[a]['togo'][i] # заполняем переходами
        
def output_ff():
    global ff, data, a
    for i in ff:
        if ff[i] not in data[a]:
            a = i
            s = True
            break
        print(i, end=" - ")
        print(data[a][ff[i]])

def end():
    global data, a
    print(data[a]["st"])
    print('Начать занова - /start')
    c = input()
    # проверяем хочет ли игрок продолжить игру
    if c == '/start':
        # если да то обнулянем прохождение
        with open('game.json', encoding='windows-1251') as f:
            data = json.load(f)
            a = data['level']
        return True
    return False

# цыкл игры
while game:
    # выводим текст
    print(data[a]["text"])
    if 'kill' in data[a]: # провека на изменения (разбирайтесь сами что это значит)
        kill(a)

    if 'music' in data[a]: # проверка на музон
        music(a)

    if 'luck' in data[a]: # проверка на удачу (хз что это)
        a = luck(a) # преходим на новый уровень
        continue
    
    if data[a]["togo"] == []: # проверка на конец игры
        q = end()
        if q == True:
            continue
        else:
            break
    completion_ff()
    # выводим переходы
    output_ff()
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
            start()
            break
        # настройки звука
        elif b == '/setting':
            setting()
            continue
        # сохраняем файл как
        elif b == '/save':
            save()
            continue
        # открфываем файл как
        elif b == '/open':
            opening()
            break
        # выводим правила
        elif b == '/rule':
            print(data['ruels'])
        # пользователь ввел хрень
        elif b not in ff:
            print('Что?')
        else:
            pass # как ты сюда попал
    if game == False:
        break
    data['level'] = ff[b]
    a = ff[b]
# сохранение прохождения
print('Сохранить (просто введите /save, если хотите сохранит, а далее название файла)')
a = input()
if a == '/save':
    save()
