from snake_module import *
import tkinter.ttk as ttk

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

main_menu.add_command(label="Выход", command=root.quit)


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
game.mainloop()  # Запускаем окно
