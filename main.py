from snake_module import *

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

# root.update()


# s.move()  # Просто вызов не работает - картинка не обновляется. Нужен root.after.


# c.bind("<Key-b>", s.change_direction)
# c.bind("<e>", s.change_direction)
# c.bind("<Return>", s.change_direction)
# c.bind("<Key-space>", s.change_direction)
# c.bind("<Control-c>", s.change_direction)
# c.bind("<KeyRelease-f>", s.change_direction)
# c.bind("<Button-1>", s.change_direction)
# c.bind("<Button-2>", s.change_direction)
# c.bind("<Double-Button>", s.change_direction)

# def init_game():
#     global s, c, apple, apple2
#     s = Snake(Segment(SEG_SIZE, SEG_SIZE, SEG_SIZE, c))  # собственно змейка
#     c.focus_set()
#     c.bind("<Key>", s.change_direction)  # или KeyPress, также можно отдельно Key-a или Key-A
#     apple = Food(s, "images/apple.png")
#     apple2 = Food(s, "images/apple.png", 5)


# init_game()


# def main():
#     global s, apple, apple2
#     s.move()
#     apple.check_snake()
#     apple2.check_snake()
#     x1, y1, x2, y2 = s.get_head_pos()
#     # Столкновение с границами экрана
#     if x1 < 0 or x2 > WIDTH or y1 < 0 or y2 > HEIGHT:
#         c.delete('all')
#         init_game()
#
#     root.after(100, main)


# main()
game = Game(c, SEG_SIZE)
game.main()

root.mainloop()  # Запускаем окно
