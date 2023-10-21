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


segments = [Segment(SEG_SIZE, SEG_SIZE), ] # создаем набор сегментов. пока одна голова

s = Snake(segments)  # собственно змейка

root.mainloop()  # Запускаем окно
