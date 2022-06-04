import numpy as np
import keyboard
from random import randint
from time import sleep
from os import system


class Playground:
    def __init__(self):
        self.playground = np.full(1, 1)
        self.obstacles_cords = []

    def set(self, size):
        if size < 5:
            raise ValueError('Playgroud will be too small')

        self.playground = np.full((size, size), ' ')

    def random_obstacles(self, num):
        # Ilość wszystkich komórek w tablicy playground oraz zapobieganie wypełnienia tablicy przeszkodami
        all_nums_in_arr = pow(self.playground.size, 2)
        if num > int(all_nums_in_arr / 3):
            raise ValueError('Too much obstacles compared to playground area')

        # Tworzenie zmiennych z wylosowanymi koordynatami dla przeszkód, im większy num tym większa tablica
        # Zapisywanie koordynatów do tablicy z której korzysta Player.collision_detection
        for x in range(0, num):
            rand1 = randint(0, self.playground.shape[0] - 1)
            rand2 = randint(0, self.playground.shape[0] - 1)
            self.obstacles_cords.append([rand1, rand2])
            self.playground[rand1][rand2] = '#'

    def show_playground(self):
        print(self.playground)


class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = 'direction'
        self.length = 1
        self.trace = [[0, 0], [0, 0]]

    def move(self, pground):
        # tablica trace wyrzucała error dlatego skracam ja dopiero po rozpoczęciu marszu
        if self.direction is not 'direction':
            # obcinanie tablicy z koordynatami węża w zależności od self.length
            self.trace = self.trace[:self.length]

        # Zapobieganie zawracania oraz ustanawianie kierunku poruszania sie węża
        if self.direction is not 'down':
            if keyboard.is_pressed('up'):
                self.direction = 'up'
        if self.direction is not 'up':
            if keyboard.is_pressed('down'):
                self.direction = 'down'
        if self.direction is not 'right':
            if keyboard.is_pressed('left'):
                self.direction = 'left'
        if self.direction is not 'left':
            if keyboard.is_pressed('right'):
                self.direction = 'right'

        if self.direction is 'up':
            self.trace.insert(0, [self.y, self.x])
            self.y -= 1
        if self.direction is 'down':
            self.trace.insert(0, [self.y, self.x])
            self.y += 1
        if self.direction is 'left':
            self.trace.insert(0, [self.y, self.x])
            self.x -= 1
        if self.direction is 'right':
            self.trace.insert(0, [self.y, self.x])
            self.x += 1

        # wąż wychodzi z drugiej strony przy wejściu w ściane
        if self.y is -1:  # up
            self.y = pground.shape[0]-1
        if self.y is pground.shape[0]:  # down
            self.y = 0
        if self.x is -1:  # left
            self.x = pground.shape[0]-1
        if self.x is pground.shape[0]:  # right
            self.x = 0

        # wyświetlanie węża w tablicy playground x - wąż
        pground[self.y][self.x] = 'x'
        # resetowanie drogi za wężem w zależności od dlugosci węża (jest skracana tablica trace)
        pground[self.trace[self.length][0]][self.trace[self.length][1]] = ' '

    def collision_detection(self, apple_cords_list, obstacles_list):
        # detection with apple
        if self.y is apple_cords_list[0] and self.x is apple_cords_list[1]:
            self.length += 1
            return 'apple'

        # detection with tail
        for e in range(0, len(self.trace)):
            if self.y is self.trace[e][0] and self.x is self.trace[e][1]:
                return 'obstacle'

        # detection with obstacles
            for f in range(0, len(obstacles_list)):
                if self.y is obstacles_list[f][0] and self.x is obstacles_list[f][1]:
                    return 'obstacle'

    def respawn(self, pground):
        flag = True
        while flag:
            self.x = randint(1, pground.shape[0] - 2)
            self.y = randint(1, pground.shape[0] - 2)
            # zapobieganie przed zrespieniem w przeszkodzie
            if pground[self.y][self.x] == '#' or pground[self.y][self.x] == 'o':
                pass
            else:
                break

    def respawn_at_point(self, x, y):
        self.x = x
        self.y = y


class Apple:
    def __init__(self):
        self.x = 0
        self.y = 0

    def respawn(self, pground):
        flag = True
        while flag:
            self.x = randint(1, pground.shape[0] - 2)
            self.y = randint(1, pground.shape[0] - 2)
            if pground[self.y][self.x] == ' ':
                pground[self.y][self.x] = 'o'
                flag = False
            else:
                flag = True


playground = Playground()
playground.set(15)
playground.random_obstacles(30)

p1 = Player()
p1.respawn(playground.playground)

appl = Apple()
appl.respawn(playground.playground)

while True:
    p1.move(playground.playground)
    if p1.collision_detection([appl.y, appl.x], playground.obstacles_cords) is 'apple':
        appl.respawn(playground.playground)
    elif p1.collision_detection([appl.y, appl.x], playground.obstacles_cords) is 'obstacle':
        print('kolizja')
        break

    playground.show_playground()
    sleep(0.4)
    system('cls')

    if keyboard.is_pressed('q'):
        break
