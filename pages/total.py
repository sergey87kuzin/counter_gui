import sqlite3
import calendar
import locale
from tkinter import Button, Label, messagebox
from src.helper import clear_frame, resource_path, date_insert
from src.global_enums.literals import (
    Titles, InfoTexts, ButtonTexts, LabelTexts
)
from configure import DB_NAME


def total(frame):
    ''' параметры для итоговой таблицы продаж '''
    clear_frame(frame)
    total_title = Label(frame, text=LabelTexts.TOTAL_TOP.value)
    total_title.grid(row=0, column=0, columnspan=2)
    month_input, year_input = date_insert(frame)
    Button(
        frame, text=ButtonTexts.SHOW_STATS.value,
        command=lambda: show_total(
            frame, month_input.get(), year_input.get()
        )
    ).grid(row=4, column=0, columnspan=2)


def show_total(frame, month, year):
    clear_frame(frame)
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    stock_total = {}
    month_total = {}
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            ''' общая таблица за весь год '''
            months = list(calendar.month_abbr)
            stocks = cursor.execute(
                'SELECT stock FROM stocks'
            ).fetchall()
            stocks = [stock[0] for stock in stocks]
            year_sales = cursor.execute(
                'SELECT month, stock, amount_sold FROM sales WHERE year=:year',
                {
                    'year': year
                }
            ).fetchall()
    except Exception:
        messagebox.showinfo(
            title=Titles.WARN_TITLE.value,
            message=InfoTexts.CHOOSE_GRAPH.value
        )
        return
    for ind, stock in enumerate(stocks):
        Label(frame, text=stock).grid(row=0, column=ind + 1)
    for sale in year_sales:
        Label(frame, text=str(sale[2])).grid(
            row=sale[0], column=stocks.index(sale[1]) + 1
        )
        if sale[1] in stock_total:
            stock_total[sale[1]] += float(sale[2])
        else:
            stock_total[sale[1]] = float(sale[2])
        if sale[0] in month_total:
            month_total[sale[0]] += float(sale[2])
        else:
            month_total[sale[0]] = float(sale[2])
    for ind, month in enumerate(months):
        Label(frame, text=month).grid(row=ind, column=0)
    for key, value in stock_total.items():
        Label(frame, text=str(value)).grid(
            row=13, column=stocks.index(key) + 1
        )
    for key, value in month_total.items():
        Label(frame, text=str(value)).grid(
            row=key, column=len(stocks) + 1
        )
