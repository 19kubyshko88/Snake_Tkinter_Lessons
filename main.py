from snake_module import *
import tkinter.ttk as ttk

# Создаем экземпляр класса для управления музыкой
music_manager = BackgroundMusic()

# Глобальная переменная для состояния чекбокса "Фоновая музыка"


# Создаем окно
root = Tk()

root.title("PythonicWay Snake")
root.resizable(False, False)

game = Game(root=root, seg_size=30)
game.add_food(img_path='images/apple.png')
game.add_food(img_path='images/donut.png', val=5)
game.main()

main_menu = Menu(root)
root.config(menu=main_menu)

records_menu = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="Рекорды", menu=records_menu)

about_menu = Menu(main_menu)
main_menu.add_cascade(label="Об игре", menu=about_menu)

settings_menu = Menu(main_menu)
main_menu.add_cascade(label="Настройки", menu=settings_menu)

main_menu.add_command(label="Выход", command=root.quit)

background_music_var = BooleanVar(value=True)  # По умолчанию включено

def show_records():
    records_window = Toplevel(root)

    table = ttk.Treeview(records_window, columns=("name", "score"))
    table.heading("name", text="Имя")
    table.heading("score", text="Счет")

    # читаем данные из файла и добавляем в таблицу
    with open("scores.txt") as f:
        for line in f:
            name, score = line.split(":")
            table.insert("", "end", values=(name, score))

    table.pack()


records_menu.add_command(label="Показать рекорды", command=show_records)


def show_about():
    about_window = Toplevel(root)
    frame = Frame(about_window, bg="white", padx=20, pady=20)

    msg = Label(frame,
                text="Эта игра была написана \n"
                                   "Павлом очень быстро",
                bg="white",
                padx=10,
                pady=10)

    msg.pack(fill="both", expand=True)

    frame.pack(fill="both", expand=True)


about_menu.add_command(label="Об игре", command=show_about)

def show_sound_settings():
    sound_settings_panel = Toplevel(root)
    frame = Frame(sound_settings_panel, bg="white", padx=20, pady=20)
    msg = Label(frame,
                text="Настройки звука",
                bg="white",
                padx=10,
                pady=10)

    msg.pack(fill="both", expand=True)

    # Переменная для хранения состояния чекбокса "Звуки игры"
    game_sounds_var = BooleanVar(value=True)  # По умолчанию включено

    # Чекбокс для фоновой музыки
    background_music_check = Checkbutton(frame,
                                         text="Фоновая музыка",
                                         variable=background_music_var,
                                         bg="white",
                                         command=lambda: music_manager.play() if background_music_var.get() else music_manager.stop())  # Управляем музыкой
    background_music_check.pack(anchor="w", pady=5)

    # Чекбокс для звуков игры
    game_sounds_check = Checkbutton(frame,
                                    text="Звуки игры",
                                    variable=game_sounds_var,
                                    bg="white")
    game_sounds_check.pack(anchor="w", pady=5)

    # Кнопка для сохранения настроек
    def save_settings():
        # Здесь можно добавить логику для сохранения настроек
        print("Фоновая музыка:", background_music_var.get())
        print("Звуки игры:", game_sounds_var.get())

    save_button = Button(frame,
                         text="Сохранить",
                         command=save_settings)
    save_button.pack(pady=10)

    frame.pack(fill="both", expand=True)


# Включаем музыку при запуске игры
music_manager.play()

settings_menu.add_command(label="Звук", command=show_sound_settings)

game.mainloop()  # Запускаем окно
