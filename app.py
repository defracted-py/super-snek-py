author = 'The app was made by Defracted-py\nGitHub: @defracted-py\n\nThe app is completely free and can be edited, just download it from the repository'

##################
### БИБЛИОТЕКИ ###
##################


from tkinter import *
import time
import random
from tkinter.font import Font
##########################
### DISCORD ИНТЕГРАЦИЯ ###
##########################
from pypresence import Presence # Библиотеки, для подключения статуса в Discord
import time


###############
### ФУНКЦИИ ###
###############


# Отрисовывает всё, выполняя остальные функции
def draw_all():
    draw_field()
    draw_food()
    draw_bonus()
    draw_snake()
    canvas.update()


# Отрисовка бонуса
def draw_bonus():
    global score
    if (score % 10 == 0) and (score != 0):
        canvas.create_oval((bonus_x + 1) * 25, (bonus_y + 1) * 25, (bonus_x + 2) * 25, (bonus_y + 2) * 25, fill="#ffe02e",
                           outline="#e3c309")


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
    global speed, logThingsToConsole

    if logThingsToConsole is True:
        print("[CHEAT] Ускоряемся...")

    speed = 0.01

    if logThingsToConsole is True:
        print(f"[CHEAT] Скорость обновления {speed} секунд")


# Немедленно повышает количество очков, чтобы победить
def cheat_win(event):
    global score, win_score, logThingsToConsole

    if logThingsToConsole is True:
        print("[CHEAT] Выполняем чит-функцию победы, жесть вы ЧиТоР, товарищ...")

    score = win_score

    if logThingsToConsole is True:
        print(f"[CHEAT] Функция выполнена, кол-во очков: {score}")


# Увеличивает количество очков на одну единицу
def cheat_add_point(event):
    global score, logThingsToConsole
    score += 1

    if logThingsToConsole is True:
        print(f"[CHEAT] Увеличено количество оков, новое кол-во: {score}")


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
    canvas.create_text(30, 13, text=f"SCORE: {score}", font="Impact 14", fill="white")


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

root.bind("<Right>", right)  # Слушатель нажатий передвижения, стрелочки
root.bind("<Left>", left)
root.bind("<Up>", up)
root.bind("<Down>", down)
root.bind("<Escape>", stop)
root.bind(["<d>", "<i>", "<e>"], speed_up)
root.bind(["<e>", "<z>", "<w>", "<i>", "<n>"], cheat_win)
root.bind(["<p>", "<o>", "<i>", "<n>", "<t>", "<s>"], cheat_add_point)


# Подключаем картинки победы и проигрыша
lose_img = PhotoImage(file="./assets/lose.png")
win_img = PhotoImage(file="./assets/win.png")

# Первоначальные значения положения змеи
table_x = [14, 15, 16]
table_y = [11, 11, 11]

# Стандартная скорость змеи, может быть изменено
speed = 0.3

# Счётчик очков
score = 0  # Стандартный, первоначальный счёт
win_score = 50  # Необходимый счёт для победы

# Перменные, позволяющие выполнять функцию паузы и основной цикл
isStopped = False
win = True

# Переменная, применяаемая для дебага/теста игры, функция для разработчиков
logThingsToConsole = True
logDiscordThingsToConsole = False

# Стандартные перменные для направления змеи
dir_x = -1
dir_y = 0

# Генерирует первое яблоко на карте
food_x, food_y = random.randint(1, 28), random.randint(0, 21)
bonus_x, bonus_y = random.randint(1, 28), random.randint(0, 21)

# DISCORD HANDSHAKE
try:
    client_id = '594064296854683650'
    RPC = Presence(client_id)
    RPC.connect()
    # Обновление статуса в Discord
    print(RPC.update(state=f"Счёт: {score}", large_image="icon", details="Начинает игру"))
except Exception:
    print('Discord not found')

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
        if logThingsToConsole is True: print(f'Количество очков: {score}')

    # Процесс «поедания» бонусных яблок
    if (table_x[0] == bonus_x) and (table_y[0] == bonus_y):
        table_x.append(1)
        table_y.append(1)
        bonus_x, bonus_y = random.randint(0, 29), random.randint(0, 21)
        score += 2
        if logThingsToConsole is True: print(f'Количество очков: {score}')

    # Проверяем, выолняется ли функция паузы
    if not isStopped:
        table_x = [table_x[0] + dir_x] + table_x
        table_y = [table_y[0] + dir_y] + table_y

        table_x.pop(-1)
        table_y.pop(-1)

    for i in range(1, len(table_x)):
        if (table_x[0] == table_x[i]) and (table_y[0] == table_y[i]):
            win = False

    # Увеличвает скорость, при увеличении счёта - усложнение игры
    if score in range(2, 10):
        speed = 0.275
        if logThingsToConsole is True: print(f"Скорость: {speed} | Счёт: {score}")
    elif score in range(10, 20):
        speed = 0.25
        if logThingsToConsole is True: print(f"Скорость: {speed} | Счёт: {score}")
    elif score in range(20, 30):
        speed = 0.225
        if logThingsToConsole is True: print(f"Скорость: {speed} | Счёт: {score}")
    elif score in range(30, 40):
        speed = 0.2
        if logThingsToConsole is True: print(f"Скорость: {speed} | Счёт: {score}")
    elif score in range(40, 45):
        speed = 0.15
        if logThingsToConsole is True: print(f"Скорость: {speed} | Счёт: {score}")
    elif score in range(45, 99999):
        speed == 0.1
        if logThingsToConsole is True: print(f"Скорость: {speed} | Счёт: {score}")

    draw_all()
    time.sleep(speed)
    canvas.delete('all')

    # Обновление статуса в Discord
    try:
        RPC.update(state=f"Счёт: {score}", details="В игре", large_image="icon")
    except Exception:
        if logDiscordThingsToConsole is True: 
            print('Discord client not found or something went wrong...')

    # Проверяем, набрали ли пользователь необходимое количество очков для победы
    if score == win_score:
        win = False

# Отрисовка изображений победы и поражения
if win is False and score < win_score:
    comic_sans = Font(family="Comic Sans MS",size=42,weight="bold")
    canvas.create_image(402, 302, image=lose_img)
    canvas.create_text(390, 450, font=comic_sans, fill="white", text=f"ваш счёт: {score}")

    # Обновление статуса в Discord
    try:
        RPC.update(state=f"Счёт: {score}", details="Поражение...", large_image="icon")
    except Exception:
        if logDiscordThingsToConsole is True: 
            print('Discord client not found or something went wrong...')
    
if win is False and score == win_score:
    canvas.create_image(402, 302, image=win_img)

    # Обновление статуса в Discord
    try: 
        RPC.update(state=f"Счёт: {score}", details="Победа!", large_image="icon")
    except Exception:
        if logDiscordThingsToConsole is True: 
            print('Discord client not found or something went wrong...')

root.mainloop()

print(author)
