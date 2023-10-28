import random
from tkinter import *
from PIL import Image, ImageTk


class Segment:
    def __init__(self, x, y, size, c):
        self.size = size
        self.x = x
        self.y = y
        self.c = c
        self.instance = c.create_rectangle(self.x, self.y,
                                           x + self.size, self.y + self.size,
                                           fill="white",
                                           # outline='white'
                                           )


class Snake:
    def __init__(self, first_segment: Segment):
        self.c = first_segment.c
        self.segment = first_segment
        self.segments = [self.segment,  # создаем набор сегментов
                         Segment(self.segment.size * 2, self.segment.size, self.segment.size, self.c),
                         Segment(self.segment.size * 3, self.segment.size, self.segment.size, self.c)
                         ]
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

    def add_segment(self):
        """ Добавляет сегмент змейке """
        # определяем последний сегмент
        last_seg = self.c.coords(self.segments[-1].instance)
        # определяем координаты куда поставить следующий сегмент
        x = last_seg[2] - self.SEG_SIZE
        y = last_seg[3] - self.SEG_SIZE
        # добавляем змейке еще один сегмент в заданных координатах
        self.segments.insert(0, Segment(x, y, self.SEG_SIZE, self.c))


class Food:
    def __init__(self, snake: Snake, canvas: Canvas, img_path):
        self.snake = snake
        self.c = canvas
        self.WIDTH, self.HEIGHT = self.c.winfo_width(), self.c.winfo_height()
        self.SIZE = self.snake.segments[0].size
        self.posx, self.posy = self.generate_rand_pos(self.WIDTH, self.HEIGHT)
        self.image = Image.open(img_path)
        self.image = self.image.resize((self.SIZE, self.SIZE), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.image)

        # Create the image item on the canvas
        self.instance = self.c.create_image(self.posx, self.posy, image=self.image, anchor=NW)
        self.coords = self.posx, self.posy, self.posx + self.SIZE, self.posy + self.SIZE

    def generate_rand_pos(self, width, height):
        rand_x = self.SIZE * (random.randint(1, (width - self.SIZE) // self.SIZE))
        rand_y = self.SIZE * (random.randint(1, (height - self.SIZE) // self.SIZE))
        return rand_x, rand_y

    def go_to_random_pos(self):
        self.posx, self.posy = self.generate_rand_pos(self.WIDTH, self.HEIGHT)
        self.coords = self.posx, self.posy, self.posx + self.SIZE, self.posy + self.SIZE
        self.c.coords(self.instance, self.posx, self.posy)

    def check_snake(self):
        head_coords = self.c.coords(self.snake.segments[-1].instance)
        # print(head_coords,  (self.posx, self.posy, self.posx + self.SIZE,self.posy + self.SIZE),
        #       head_coords == (self.posx, self.posy, self.posx + self.SIZE,self.posy + self.SIZE))
        if all(head_coor == food_coor for head_coor, food_coor in zip(head_coords, self.coords)):
            self.go_to_random_pos()
            self.snake.add_segment()
