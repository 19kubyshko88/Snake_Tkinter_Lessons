from tkinter import *

# Создаем окно
root = Tk()

root.title("PythonicWay Snake")
root.resizable(0, 0)


WIDTH = 800  # ширина экрана
HEIGHT = 600  # высота экрана
SEG_SIZE = 20  # Размер сегмента змейки

# root.geometry(f'{WIDTH}x{HEIGHT}')


c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#003300")
# c.pack()
# c.place(x=100, y=0)
c.grid()  # Без этого canvas не появится. Альтернатива pack()  и place()

# root.update()
# print(root.geometry())
root.mainloop()  # Запускаем окно
