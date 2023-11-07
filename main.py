from snake_module import *

# Создаем окно
root = Tk()

root.title("PythonicWay Snake")
root.resizable(False, False)

game = Game(root=root)
game.add_food(img_path='images/apple.png')
game.add_food(img_path='images/donut.png', val=5)
game.main()

game.mainloop()  # Запускаем окно
