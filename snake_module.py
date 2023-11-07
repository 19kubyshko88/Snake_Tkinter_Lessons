import random
from tkinter import *
from PIL import Image, ImageTk


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
        self.image = self.image.resize((Game.SEG_SIZE, Game.SEG_SIZE), Image.LANCZOS)
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
    # def __new__(cls, *args, **kwargs):  # Можно зaдать канву до создания объекта класса (до __init__),  вместо Game.c = c.
    #     cls.root = kwargs['root']
    #     cls.WIDTH = 800  # ширина экрана
    #     cls.HEIGHT = 600  # высота экрана
    #     cls.SEG_SIZE = 20  # Размер сегмента змейки
    #
    #     cls.c = Canvas(cls.root, width=cls.WIDTH, height=cls.HEIGHT, bg="#003300")
    #     cls.c.grid()  # Без этого canvas не появится. Альтернатива pack()  и place()
    #     cls.c.update()
    #     cls.text_x, cls.text_y = cls.WIDTH * 0.9, cls.HEIGHT * 0.1
    #     return super().__new__(cls)

    def __init__(self, root, c: Canvas, segment_size):
        super().__init__(root)
        self.start_new = True
        self.foods = []
        self.poison = []
        self.img_food_path = []
        Game.c = c
        Game.WIDTH = self.c.winfo_width()
        Game.HEIGHT = self.c.winfo_height()
        Game.SEG_SIZE = segment_size
        Game.text_x, Game.text_y = Game.WIDTH * 0.9, Game.HEIGHT * 0.1

    def add_food(self, img_path="images/apple.png", val=1):
        self.img_food_path.append(img_path)
        self.foods.append(Food(img_path, val))

    def init_game(self):
        # инициализация объектов
        self.score = 0
        self.score_text = self.c.create_text(Game.text_x, Game.text_y, text="Счет: 0", fill="white")
        self.s = Snake(Segment(Game.SEG_SIZE, Game.SEG_SIZE))  # собственно змейка
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
        self.score_text = self.c.create_text(Game.text_x, Game.text_y, text=f"Счет: {self.score}", fill="white")

    def main(self):
        if self.start_new:
            self.init_game()
            self.start_new = False
        self.s.move()
        # [food.check_snake() for food in self.foods]
        self.check_feeding()
        x1, y1, x2, y2 = self.s.get_head_pos()
        if x1 < 0 or x2 > self.c.winfo_width() or y1 < 0 or y2 > self.c.winfo_height():
            for segment in self.s.segments:
                self.c.delete(segment.instance)
            self.c.delete(self.score_text)
            # [self.c.delete(food) for food in self.foods]
            self.start_new = True
        self.c.after(100, self.main)
