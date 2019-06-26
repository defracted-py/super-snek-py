__author__ = 'The app was made by Defracted\nGitHub: @runic-tears\n\nThe app is completely free and can be edited, just download it from the repository'

##################
### БИБЛИОТЕКИ ###
##################

from tkinter import *
import time
import random

###############
### ФУНКЦИИ ###
###############


# Отрисовывает всё, выполняя остальные функции
def draw_all():
    draw_field()
    draw_food()
    draw_snake()
    canvas.update()


# Отрисовывает один элемент змеи
def draw_elements(i, j, color, outline_color):
    canvas.create_oval((i+1)*25, (j+1)*25, (i+2)*25, (j+2)*25, fill=color, outline=outline_color)


# Отрисовывает змею
def draw_snake():
    global table_x, table_y
    for i in range(1, len(table_x)):
        # Отрисовка тела змеи
        draw_elements(table_x[i], table_y[i], "#96d05e", "#96d05e")
    # Отрисовка головы змеи
    draw_elements(table_x[0], table_y[0], "#c7e162", "#c7e162")


# Увелчивает скорость передвижения змеи, необходимо для более просто тестирования
def speed_up(event):
    print("Ускоряемся...")
    global speed
    speed = 0.05
    print(f"Скорость обновления {speed} секунд")


# Немедленно повышает количество очков, чтобы победить
def cheat_win(event):
    print("Выполняем чит-функцию победы, жесть вы ЧиТоР, товарищ...")
    global score, win_score
    score = win_score
    print(f"Функция выполнена, кол-во очков: {score}")


# Поворачивает передвижении змеи в правую сторону
def right(event):
    # Предоствращение возможности повернуть в противоположную сторону, что может «убить» змею
    global dir_x, dir_y
    if dir_x == -1:
        return
    dir_x = 1
    dir_y = 0


# Идентично функции выше, только направляет в левую сторону
def left(event):
    global dir_x, dir_y
    if dir_x == 1:
        return
    dir_x = -1
    dir_y = 0


# Идентично функции выше, только направляет вверх
def up(event):
    global dir_x, dir_y
    if dir_y == 1:
        return
    dir_x = 0
    dir_y = -1


# Идентично функции выше, только направляет вниз
def down(event):
    global dir_x, dir_y
    if dir_y == -1:
        return
    dir_x = 0
    dir_y = 1


# Создаёт границу мира
def draw_field():
    global score
    canvas.create_rectangle(0, 0, 32*25, 24*25, fill="#617c52")
    canvas.create_rectangle(25, 25, 31*25, 23*25, fill="#789965", outline='#789965')
    canvas.create_text(30, 13, text=f"СЧЁТ: {score}", font="Impact 14", fill="white")


# Создание еды для змейки
def draw_food():
    canvas.create_oval((food_x+1)*25, (food_y+1)*25, (food_x+2)*25, (food_y+2)*25, fill="#df4f49", outline="#b53732")


# Пауза
def stop(event):
    global isStopped, win
    if isStopped:
        isStopped = False
    else:
        isStopped = True


root = Tk()
root.iconbitmap('./assets/favicon.ico')  # Иконка окна
canvas = Canvas(width=32*25, height=24*25, background='#617c52')  # Размер окна
canvas.pack()
root.title("Super Snek")  # Название окна
root.resizable(False, False)  # Убирает возможность изменять размер окна

root.bind("<Right>", right)
root.bind("<Left>", left)
root.bind("<Up>", up)
root.bind("<Down>", down)
root.bind("<Escape>", stop)
root.bind(["<d>", "<i>", "<e>"], speed_up)
root.bind(["<e>", "<z>", "<w>", "<i>", "<n>"], cheat_win)


# Подключаем картинки победы и проигрыша
lose_img = PhotoImage(file="./assets/lose.png")
win_img = PhotoImage(file="./assets/win.png")

# Первоначальные значения положения змеи
table_x = [14, 15, 16]
table_y = [11, 11, 11]

# Стандартная скорость змеи, может быть изменено
speed = 0.2

# Счётчик очков
score = 0  # Текущий
win_score = 15  # Необходимый для победы

# Перменные, позволяющие выполнять функцию паузы и основной цикл
isStopped = False
win = True

# Стандартные перменные для направления змеи
dir_x = -1
dir_y = 0

# Генерирует первое яблоко на карте
food_x, food_y = random.randint(1, 28), random.randint(0, 21)

# Основной цикл всего приложения
while win:
    # Проверяем, не врезалась ли змея в стены
    if (table_x[0] == 0) and (dir_x == -1):
        win = False
    if (table_x[0] == 29) and (dir_x == 1):
        win = False
    if (table_y[0] == 0) and (dir_y == -1):
        win = False
    if (table_y[0] == 21) and (dir_y == 1):
        win = False

    # Процесс «поедания» яблок
    if (table_x[0] == food_x) and (table_y[0] == food_y):
        table_x.append(1)
        table_y.append(1)
        food_x, food_y = random.randint(0, 29), random.randint(0, 21)
        score += 1
        print(f'Количество очков: {score}')

    # ПРоверяем, выолняется ли функция паузы
    if not isStopped:
        table_x = [table_x[0] + dir_x] + table_x
        table_y = [table_y[0] + dir_y] + table_y

        table_x.pop(-1)
        table_y.pop(-1)

    for i in range(1, len(table_x)):
        if (table_x[0] == table_x[i]) and (table_y[0] == table_y[i]):
            win = False

    draw_all()
    time.sleep(speed)
    canvas.delete('all')

    # Проверяем, набрали ли пользователь необходимое количество очков для победы
    if score == win_score:
        win = False

# Отрисовка изображений победы и поражения
if win is False and score < win_score:
    canvas.create_image(402, 302, image=lose_img)
if win is False and score == win_score:
    canvas.create_image(402, 302, image=win_img)

root.mainloop()

print(__author__)
