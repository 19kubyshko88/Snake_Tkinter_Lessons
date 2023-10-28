import random
from tkinter import *

# Создаем окно
root = Tk()

root.title("PythonicWay Snake")
root.resizable(False, False)


WIDTH = 800  # ширина экрана
HEIGHT = 600  # высота экрана
SEG_SIZE = 20  # Размер сегмента змейки

# root.geometry(f'{WIDTH}x{HEIGHT}')


c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#003300")
c.grid()  # Без этого canvas не появится. Альтернатива pack()  и place()

root.update()


class Segment(object):
    def __init__(self, x, y, size):
        self.size = size
        self.instance = c.create_rectangle(x, y,
                                           x + self.size, y + self.size,
                                           fill="white",
                                           # outline='white'
                                           )


class Snake(object):
    def __init__(self, segments):
        self.segments = segments
        self.vector = 'right'

    def move(self):
        """ Двигает змейку в заданном направлении """
        for index in range(len(self.segments) - 1):  # перебираем все сегменты кроме первого
            segment = self.segments[index].instance
            x1, y1, x2, y2 = c.coords(self.segments[index + 1].instance)
            c.coords(segment, x1, y1, x2, y2)  # задаем каждому сегменту позицию сегмента стоящего после него

        x1, y1, x2, y2 = c.coords(self.segments[-1].instance)  # получаем координаты сегмента головы
        match self.vector:
            case 'right':
                c.coords(self.segments[-1].instance,  # при перемещении головы меняются координаты
                         x1 + SEG_SIZE, y1,                   # левого верхнего и
                         x2 + SEG_SIZE, y2)                      # правого нижнего угла прямоугольника.
            case 'down':
                c.coords(self.segments[-1].instance,
                         x1, y1 + SEG_SIZE,
                         x2, y2 + SEG_SIZE)
            case 'up':
                c.coords(self.segments[-1].instance,
                         x1, y1 - SEG_SIZE,
                         x2, y2 - SEG_SIZE)
            case 'left':
                c.coords(self.segments[-1].instance,
                         x1 - SEG_SIZE, y1,
                         x2 - SEG_SIZE, y2)

    def change_direction(self, event):
        # print('Ты нажал кнопку', event.char.lower())
        match  event.char.lower():
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
        self.SiZE = self.snake.segments[0].size
        self.posx, self.posy = self.generate_rand_pos(self.WIDTH, self.HEIGHT)
        self.instance = c.create_oval(self.posx, self.posy,  # еда - это кружочек красного цвета
                                      self.posx + SEG_SIZE,
                                      self.posy + SEG_SIZE,
                                      fill="red")

    def generate_rand_pos(self, width, height):
        rand_x = self.SiZE * (random.randint(1, (width - self.SiZE) // self.SiZE))
        rand_y = self.SiZE * (random.randint(1, (height - self.SiZE) // self.SiZE))
        return rand_x, rand_y

    def go_to_random_pos(self):
        self.posx, self.posy = self.generate_rand_pos(self.WIDTH, self.HEIGHT)
        self.c.coords(self.instance,
                      self.posx, self.posy,
                      self.posx + SEG_SIZE,
                      self.posy + SEG_SIZE)

    def check_snake(self):
        head_coords = self.c.coords(self.snake.segments[-1].instance)
        # print(head_coords)
        if head_coords == self.c.coords(self.instance):
            self.go_to_random_pos()


segments = [Segment(SEG_SIZE, SEG_SIZE, SEG_SIZE),  # создаем набор сегментов
            Segment(SEG_SIZE * 2, SEG_SIZE, SEG_SIZE),
            Segment(SEG_SIZE * 3, SEG_SIZE, SEG_SIZE)
            ]

s = Snake(segments)  # собственно змейка
# s.move()  # Просто вызов не работает - картинка не обновляется. Нужен root.after.

c.focus_set()
c.bind("<Key>", s.change_direction)  # или KeyPress, также можно отдельно Key-a или Key-A
# c.bind("<Key-b>", s.change_direction)
# c.bind("<e>", s.change_direction)
# c.bind("<Return>", s.change_direction)
# c.bind("<Key-space>", s.change_direction)
# c.bind("<Control-c>", s.change_direction)
# c.bind("<KeyRelease-f>", s.change_direction)
# c.bind("<Button-1>", s.change_direction)
# c.bind("<Button-2>", s.change_direction)
# c.bind("<Double-Button>", s.change_direction)

apple = Food(s, c)


def main():
    s.move()
    apple.check_snake()
    root.after(100, main)


main()

root.mainloop()  # Запускаем окно
