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
        # print('snake c id', id(self.c))


class Snake:
    def __init__(self, first_segment: Segment):
        self.c: Canvas = first_segment.c
        # print('snake c id', id(self.c))
        self.segment = first_segment
        self.segments = [self.segment,  # создаем набор сегментов
                         Segment(self.segment.size * 2, self.segment.size, self.segment.size, self.c),
                         Segment(self.segment.size * 3, self.segment.size, self.segment.size, self.c)
                         ]
        self.head = self.segments[-1].instance
        self.vector = 'stop'
        self.SEG_SIZE = self.segments[0].size
        self.score = 0
        self.score_text = self.c.create_text(50, 20, text="Счет: 0", fill="white")

    def move(self):
        """ Двигает змейку в заданном направлении """
        if self.vector == 'stop':
            return
        for index in range(len(self.segments) - 1):  # перебираем все сегменты кроме первого
            segment = self.segments[index].instance
            x1, y1, x2, y2 = self.c.coords(self.segments[index + 1].instance)
            self.c.coords(segment, x1, y1, x2, y2)  # задаем каждому сегменту позицию сегмента стоящего после него

        x1, y1, x2, y2 = self.get_head_pos()  # получаем координаты сегмента головы
        match self.vector:
            case 'right':
                self.c.coords(self.head,  # при перемещении головы меняются координаты
                              x1 + self.SEG_SIZE, y1,  # левого верхнего и
                              x2 + self.SEG_SIZE, y2)  # правого нижнего угла прямоугольника.
            case 'down':
                self.c.coords(self.head,
                              x1, y1 + self.SEG_SIZE,
                              x2, y2 + self.SEG_SIZE)
            case 'up':
                self.c.coords(self.head,
                              x1, y1 - self.SEG_SIZE,
                              x2, y2 - self.SEG_SIZE)
            case 'left':
                self.c.coords(self.head,
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
        # определяем координаты куда поставить следующий сегмент
        x, y, _, _ = self.get_head_pos()
        # добавляем змейке еще один сегмент в заданных координатах
        self.segments.insert(0, Segment(x, y, self.SEG_SIZE, self.c))

    def change_score(self, val=1):
        self.c.delete(self.score_text)
        self.score += val
        self.score_text = self.c.create_text(50, 20, text=f"Счет: {self.score}", fill="white")

    def get_head_pos(self):
        return self.c.coords(self.head)


class Food:
    def __init__(self, snake: Snake, img_path, val=1):
        self.snake = snake
        self.c = snake.c
        self.WIDTH, self.HEIGHT = self.c.winfo_width(), self.c.winfo_height()
        self.SIZE = self.snake.segments[0].size
        self.posx, self.posy = self.generate_rand_pos(self.WIDTH, self.HEIGHT)
        self.image = Image.open(img_path)
        self.image = self.image.resize((self.SIZE, self.SIZE), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.image)
        self.val = val

        # Create the image item on the canvas
        self.instance = self.snake.c.create_image(self.posx, self.posy, image=self.image, anchor=NW)
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
            self.snake.change_score(self.val)
            self.go_to_random_pos()
            self.snake.add_segment()
