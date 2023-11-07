from snake_module import *

# Создаем окно
root = Tk()

root.title("PythonicWay Snake")
root.resizable(False, False)


WIDTH = 800  # ширина экрана
HEIGHT = 600  # высота экрана
SEG_SIZE = 20  # Размер сегмента змейки

c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#003300")
c.grid()  # Без этого canvas не появится. Альтернатива pack()  и place()
c.update()

game = Game(root, c=c, segment_size=SEG_SIZE)

game.add_food(img_path='images/apple.png')
game.add_food(img_path='images/apple.png', val=5)
game.main()

game.mainloop()  # Запускаем окно
