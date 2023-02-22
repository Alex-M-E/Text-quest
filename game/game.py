import json
import random as rd
import time
from pygame import mixer 

mixer.init()
mixer.music.load('music/dobro-pojalovat-na-server-shizofreniya-original.mp3')
mixer.music.play()

sound = True

with open('game.json', encoding='windows-1251') as f:
    data = json.load(f)

print(data['ruels'])
# цикл игры
a = data['level']
game = True
while game:
    print(data[a]["text"])
    if 'kill' in data[a]:
        d = data['kill' + data[a]['kill']]
        for i in d:
            exec(i)
    if 'music' in data[a]:
        if sound is True:
            mixer.init()
            mixer.music.load('music/' + data[a]['music'])
            mixer.music.play()
    if 'luck' in data[a]:
        a = data[a]['luck'][rd.randint(0, len(data[a]["luck"])) - 1]
        continue
    if data[a]["togo"] == []:
        print(data[a]["st"])
        print('Начать занова - /start')
        c = input()
        if c == '/start':
            with open('game.json') as f:
                data = json.load(f)
            a = data['level']
            continue
        else:
            break
    s = False
    for i in data[a]['togo']:
        if i not in data[a]:
            a = i
            s = True
            break
        print(i, end=" - ")
        print(data[a][i])
    if s is True:
        continue
    b = ""
    while b not in data[a]["togo"]:
        b = input()
        if b == '/exit':
            game = False
            b = a
            break
        elif b == '/start':
            with open('game.json', encoding='windows-1251') as f:
                data = json.load(f)
            b = data['level']
            break
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
        elif b == '/save':
            c = input()
            with open(c + '.json', 'w') as file:
                json.dump(data, file, ensure_ascii=False)
            continue
        elif b == '/open':
            c = input()
            with open(c + '.json') as file:
                data = json.load(file)
                b = data['level']
            break
        elif b == '/rule':
            print(data['ruels'])
        elif b not in data[a]["togo"]:
            print('Что?')
        else:
            pass
    data['level'] = b
    a = b
print('Сохранить (просто введите /save, если хотите сохранит, а далее название файла)')
a = input()
if a == '/save':
    c = input()
    with open(c + '.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False)
