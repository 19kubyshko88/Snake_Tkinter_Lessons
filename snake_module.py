import random, os
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox as mb


class Segment:
    def __init__(self, x, y):
        self.size = Game.SEG_SIZE
        self.__c = Game.c
        self.x = x
        self.y = y
        self.instance = self.__c.create_rectangle(self.x, self.y,
                                                  x + self.size, self.y + self.size,
                                                  fill="white",
                                                  # outline='white'
                                                  )
        # print('snake c id', id(self.c))


class Snake:
    def __init__(self, first_segment: Segment):
        # print(dir(first_segment))  # возвращает список имён (атрибутов) в алфавитном порядке
        # self.c: Canvas = first_segment._Segment__c  # Доступ к private аттрибуту
        self.__c: Canvas = Game.c
        self.segment = first_segment
        self.segments = [self.segment,  # создаем набор сегментов
                         Segment(Game.SEG_SIZE * 2, self.segment.size),
                         Segment(self.segment.size * 3, self.segment.size)
                         ]
        self.head = self.segments[-1].instance
        self.vector = 'stop'
        self.SEG_SIZE = self.segments[0].size

    def move(self):
        """ Двигает змейку в заданном направлении """
        if self.vector == 'stop':
            return
        for index in range(len(self.segments) - 1):  # перебираем все сегменты кроме первого
            segment = self.segments[index].instance
            x1, y1, x2, y2 = self.__c.coords(self.segments[index + 1].instance)
            self.__c.coords(segment, x1, y1, x2, y2)  # задаем каждому сегменту позицию сегмента стоящего после него

        x1, y1, x2, y2 = self.get_head_pos()  # получаем координаты сегмента головы
        match self.vector:
            case 'right':
                self.__c.coords(self.head,  # при перемещении головы меняются координаты
                                x1 + self.SEG_SIZE, y1,  # левого верхнего и
                                x2 + self.SEG_SIZE, y2)  # правого нижнего угла прямоугольника.
            case 'down':
                self.__c.coords(self.head,
                                x1, y1 + self.SEG_SIZE,
                                x2, y2 + self.SEG_SIZE)
            case 'up':
                self.__c.coords(self.head,
                                x1, y1 - self.SEG_SIZE,
                                x2, y2 - self.SEG_SIZE)
            case 'left':
                self.__c.coords(self.head,
                                x1 - self.SEG_SIZE, y1,
                                x2 - self.SEG_SIZE, y2)

    def not_in_border(self):
        x1, y1, x2,y2 = self.get_head_pos()
        return x1 < 0 or x2 > self.__c.winfo_width() or y1 < 0 or y2 > self.__c.winfo_height()

    def bite_yourself(self):
        for index in range(len(self.segments) - 1):
            if self.__c.coords(self.segments[index].instance) == self.get_head_pos():
                return True
        return False

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
        self.segments.insert(0, Segment(x, y))

    def get_head_pos(self):
        return self.__c.coords(self.head)


class Food:
    def __init__(self, img_path, val=1):
        self.c = Game.c
        self.WIDTH, self.HEIGHT = self.c.winfo_width(), self.c.winfo_height()
        self.posx, self.posy = self.generate_rand_pos(self.WIDTH, self.HEIGHT)
        self.image = Image.open(img_path)
        k = max(self.image.width, self.image.height) // Game.SEG_SIZE
        self.image = self.image.resize((self.image.width // k, self.image.height // k), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.image)
        self.val = val

        # Create the image item on the canvas
        self.instance = self.c.create_image(self.posx, self.posy, image=self.image, anchor=NW)
        self.coords = self.posx, self.posy, self.posx + Game.SEG_SIZE, self.posy + Game.SEG_SIZE

    def generate_rand_pos(self, width, height):
        rand_x = Game.SEG_SIZE * (random.randint(1, (width - Game.SEG_SIZE) // Game.SEG_SIZE))
        rand_y = Game.SEG_SIZE * (random.randint(1, (height - Game.SEG_SIZE) // Game.SEG_SIZE))
        return rand_x, rand_y

    def go_to_random_pos(self):
        self.posx, self.posy = self.generate_rand_pos(self.WIDTH, self.HEIGHT)
        self.coords = self.posx, self.posy, self.posx + Game.SEG_SIZE, self.posy + Game.SEG_SIZE
        self.c.coords(self.instance, self.posx, self.posy)


class Game(Frame):
    root: Tk = None
    c = None
    score_text = None
    WIDTH = 800  # ширина экрана
    HEIGHT = 600  # высота экрана
    SEG_SIZE = 20  # Размер сегмента змейки
    text_x, text_y = WIDTH * 0.9, HEIGHT * 0.1
    if not os.path.exists("scores.txt"):
        open("scores.txt", "w").close()

    def __new__(cls, *args, **kwargs):
        cls.root = kwargs['root']
        cls.c = Canvas(cls.root, width=cls.WIDTH, height=cls.HEIGHT, bg="#003300")
        cls.c.grid()  # Без этого canvas не появится. Альтернатива pack()  и place()
        cls.c.update()  # Нужно чтобы канва приняла размер>0. Иначе ошибка.
        return super().__new__(cls)

    def __init__(self, root):
        super().__init__(root)
        self.start_new = True
        self.foods = []
        self.poison = []
        self.img_food_path = []

    def add_food(self, img_path="images/apple.png", val=1):
        self.img_food_path.append(img_path)
        self.foods.append(Food(img_path, val))

    def init_game(self):
        # инициализация объектов
        self.score = 0
        self.score_text = self.c.create_text(Game.text_x, self.text_y, text="Счет: 0", fill="white")
        self.s = Snake(Segment(self.SEG_SIZE, self.SEG_SIZE))  # собственно змейка
        self.c.focus_set()
        self.c.bind("<Key>", self.s.change_direction)  # или KeyPress, также можно отдельно Key-a или Key-A
        if not self.foods:
            self.add_food()
        else:
            [food.go_to_random_pos() for food in self.foods]
        [Food(im_path).go_to_random_pos() for im_path in self.img_food_path]
        # self.apple2 = Food(self.s, "images/apple.png", 5)

    def check_feeding(self):
        head_coords = self.c.coords(self.s.head)
        for food in self.foods:
            if all(head_coor == food_coor for head_coor, food_coor in zip(head_coords, food.coords)):
                self.change_score(food.val)
                food.go_to_random_pos()
                self.s.add_segment()

    def change_score(self, val=1):
        self.c.delete(self.score_text)
        self.score += val
        self.score_text = self.c.create_text(self.text_x, self.text_y, text=f"Счет: {self.score}", fill="white")

    def show_name_input(self):
        top = Toplevel(self.root)
        # получаем координаты холста
        x = self.root.winfo_x()
        y = self.root.winfo_y()

        # размещаем окно ввода поверх холста
        x = self.root.winfo_x() + self.root.winfo_width()//2
        y = self.root.winfo_y() + self.root.winfo_height()//2
        top.geometry(f"+{x}+{y}")

        top.title("Введи имя")

        name = StringVar()
        entry = Entry(top, textvariable=name)
        entry.pack()

        button = Button(top, text="Ok", command=lambda: self.save_result(name.get(), top))
        button.pack()

        button.focus_force()  # сфокусировать ввод с клавиатуры именно на окно top
        top.grab_set()   # для блокировки всех других окон
        top.wait_window()

    def save_result(self, name, wind):
        score_str = f"{name}: {self.score}"
        with open('scores.txt', 'r+', encoding='utf-8') as f:
            record_list = f.readlines()
            record_list.append(score_str)
            record_dict = {line.split(':')[0].strip(): int(line.split(':')[1].strip()) for line in record_list}
            sorted_records = dict(sorted(record_dict.items(), key=lambda item: item[1], reverse=True))
            f.seek(0)
            dict_len = len(sorted_records)
            counter = 0
            for name, scores in sorted_records.items():
                if counter < dict_len:
                    f.write(f'{name}:{scores}\n')
                    counter += 1
                else:
                    f.write(f'{name}:{scores}')
        wind.destroy()

    def main(self):
        if self.start_new:
            self.init_game()
            self.start_new = False
        self.check_feeding()
        self.s.move()

        if self.s.not_in_border() or self.s.bite_yourself():
            self.show_name_input()
            answer = mb.askyesno(title="Конец",
                                 message="Продолжить игру?")
            if answer:
                for segment in self.s.segments:
                    self.c.delete(segment.instance)
                self.c.delete(self.score_text)
                self.start_new = True
            else:
                # self.root.quit()
                self.root.destroy()

        self.c.after(100, self.main)
