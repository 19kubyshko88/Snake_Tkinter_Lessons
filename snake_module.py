import random
from tkinter import *


class Segment():
    def __init__(self, x, y, size, c):
        self.size = size
        self.instance = c.create_rectangle(x, y,
                                           x + self.size, y + self.size,
                                           fill="white",
                                           # outline='white'
                                           )


class Snake():
    def __init__(self, segments, c):
        self.c = c
        self.segments = segments
        self.vector = 'right'
        self.SEG_SIZE = self.segments[0].size

    def move(self):
        """ Двигает змейку в заданном направлении """
        for index in range(len(self.segments) - 1):  # перебираем все сегменты кроме первого
            segment = self.segments[index].instance
            x1, y1, x2, y2 = self.c.coords(self.segments[index + 1].instance)
            self.c.coords(segment, x1, y1, x2, y2)  # задаем каждому сегменту позицию сегмента стоящего после него

        x1, y1, x2, y2 = self.c.coords(self.segments[-1].instance)  # получаем координаты сегмента головы
        match self.vector:
            case 'right':
                self.c.coords(self.segments[-1].instance,  # при перемещении головы меняются координаты
                              x1 + self.SEG_SIZE, y1,  # левого верхнего и
                              x2 + self.SEG_SIZE, y2)  # правого нижнего угла прямоугольника.
            case 'down':
                self.c.coords(self.segments[-1].instance,
                              x1, y1 + self.SEG_SIZE,
                              x2, y2 + self.SEG_SIZE)
            case 'up':
                self.c.coords(self.segments[-1].instance,
                              x1, y1 - self.SEG_SIZE,
                              x2, y2 - self.SEG_SIZE)
            case 'left':
                self.c.coords(self.segments[-1].instance,
                              x1 - self.SEG_SIZE, y1,
                              x2 - self.SEG_SIZE, y2)

    def change_direction(self, event):
        # print('Ты нажал кнопку', event.char.lower())
        match event.char.lower():
            case 'a':
                print('влево')
                self.vector = 'left'
            case 'w':
                print('вверх')
                self.vector = 'up'
            case 's':
                print('вниз')
                self.vector = 'down'
            case 'd':
                print('направо')
                self.vector = 'right'


class Food:
    def __init__(self, snake: Snake, canvas: Canvas):
        self.snake = snake
        self.c = canvas
        self.WIDTH, self.HEIGHT = self.c.winfo_width(), self.c.winfo_height()
        self.SIZE = self.snake.segments[0].size
        self.posx, self.posy = self.generate_rand_pos(self.WIDTH, self.HEIGHT)
        self.instance = self.c.create_oval(self.posx, self.posy,  # еда - это кружочек красного цвета
                                           self.posx + self.SIZE,
                                           self.posy + self.SIZE,
                                           fill="red")

    def generate_rand_pos(self, width, height):
        rand_x = self.SIZE * (random.randint(1, (width - self.SIZE) // self.SIZE))
        rand_y = self.SIZE * (random.randint(1, (height - self.SIZE) // self.SIZE))
        return rand_x, rand_y

    def go_to_random_pos(self):
        self.posx, self.posy = self.generate_rand_pos(self.WIDTH, self.HEIGHT)
        self.c.coords(self.instance,
                      self.posx, self.posy,
                      self.posx + self.SIZE,
                      self.posy + self.SIZE)

    def check_snake(self):
        head_coords = self.c.coords(self.snake.segments[-1].instance)
        # print(head_coords)
        if head_coords == self.c.coords(self.instance):
            self.go_to_random_pos()
