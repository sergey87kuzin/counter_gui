import sqlite3
import logging
from tkinter import (
    Button, Tk, W, LabelFrame, messagebox
)
from pages import (
    add_loads, month_stats, year_stats, add_income,
    create_stock, graphic, total
)

GRAPHICS = ['Год суммарно', 'Месяц по стокам']

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    filemode='w',
    format=('%(asctime)s, %(levelname)s, %(name)s, %(message)s,' +
            '%(funcName)s, %(lineno)d')
)

logging.info('app started')

conn = sqlite3.connect('gui.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS stocks(stock text)')
cursor.execute('''CREATE TABLE IF NOT EXISTS loads(
    day integer, month integer, year integer, photo_load, video_load
    )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS sales(
    month integer, year integer,
    photo_sold, video_sold, amount_sold, stock text)''')
conn.commit()
conn.close()

logging.info('db is available')

root = Tk()
root.title('Счетчик для стоков')
second_screen = Tk()
second_screen.title('Результат')
second_screen.eval('tk::PlaceWindow . center')


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        second_screen.destroy()
        root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
second_screen.protocol("WM_DELETE_WINDOW", on_closing)
frame = LabelFrame(second_screen, text='Ваши данные', padx=5, pady=5)
frame.pack()

add_loads_button = Button(
    root, text='Добавить загрузки',
    command=lambda: add_loads(frame), width=25
)
month_stats_button = Button(
    root, text='Посмотреть данные месяца',
    command=lambda: month_stats(frame), width=25
)
year_stats_button = Button(
    root, text='Посмотреть данные года',
    command=lambda: year_stats(frame), width=25
)
add_income_button = Button(
    root, text='Внести доходы',
    command=lambda: add_income(frame), width=25
)
create_stock_button = Button(
    root, text='Создать сток',
    command=lambda: create_stock(frame), width=25
)
graphic_button = Button(
    root, text='График', width=25,
    command=lambda: graphic(frame)
)
total_button = Button(
    root, text='Суммарный итог', width=25,
    command=lambda: total(frame)
)
buttons = [add_loads_button, month_stats_button, year_stats_button,
           add_income_button, create_stock_button, graphic_button,
           total_button]
for ind, button in enumerate(buttons):
    button.grid(row=ind, column=0, sticky=W)
root.mainloop()
