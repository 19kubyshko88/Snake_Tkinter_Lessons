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


class Segment(object):
    def __init__(self, x, y):
        self.instance = c.create_rectangle(x, y,
                                           x + SEG_SIZE, y + SEG_SIZE,
                                           fill="white",
                                           # outline='white'
                                           )


class Snake(object):
    def __init__(self, segments):
        self.segments = segments

    def move(self):
        x1, y1, x2, y2 = c.coords(self.segments[0].instance)  # получаем координаты сегмента головы
        c.coords(self.segments[-1].instance,  # при перемещении головы меняются координаты
                 x1 + SEG_SIZE, y1,                   # левого верхнего и
                 x2 + SEG_SIZE, y2)                      # правого нижнего угла прямоугольника.


segments = [Segment(SEG_SIZE, SEG_SIZE), ]  # создаем набор сегментов. пока одна голова

s = Snake(segments)  # собственно змейка
# s.move()  # Просто вызов не работает - картинка не обновляется. Нужен root.after.


def main():
    s.move()
    root.after(100, main)


main()

root.mainloop()  # Запускаем окно
