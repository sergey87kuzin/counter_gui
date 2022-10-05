import os
import sys
import sqlite3
from datetime import date
import calendar
from tkmacosx import CircleButton
from tkinter import Entry, Label, W, messagebox
from src.global_enums.literals import (
    Titles, InfoTexts, LabelTexts, ButtonTexts
)


def start_sql():
    try:
        conn = sqlite3.connect(resource_path('gui.db'))
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS stocks(stock text)')
        cursor.execute('''CREATE TABLE IF NOT EXISTS loads(
            day integer, month integer, year integer, photo_load,
            video_load)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS sales(
            month integer, year integer,
            photo_sold, video_sold, amount_sold, stock text)''')
        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showinfo(
            title=Titles.WARN_TITLE.value,
            message=str(e)
        )


def clear_frame(frame):
    ''' очистка рамки перед повторным использованием '''
    for widget in frame.winfo_children():
        widget.destroy()


def date_insert(frame):
    ''' добавление полей даты '''
    today = str(date.today())
    curr_year = today[2:4]
    curr_month = today[5:7]
    month_text = Label(frame, text=LabelTexts.MONTH.value)
    year_text = Label(frame, text=LabelTexts.YEAR.value)
    month_input = Entry(frame, width=2)
    month_input.insert(0, curr_month)
    year_input = Entry(frame, width=2)
    year_input.insert(0, curr_year)
    texts = (month_text, year_text)
    entries = (month_input, year_input)
    registrate_inputs(texts, entries, 2)
    return month_input, year_input


def registrate_inputs(texts, entries, off):
    ''' расположение полей на рамке '''
    for ind, text in enumerate(texts):
        text.grid(row=ind+off, column=0, sticky=W)
    for ind, entry in enumerate(entries):
        entry.grid(row=ind+off, column=1, sticky=W)


def month_year_validate(month, year):
    try:
        month = int(month)
        year = int(year)
    except Exception:
        messagebox.showinfo(
            title=Titles.WARN_TITLE.value,
            message=InfoTexts.WRONG_TYPE.value
        )
        return True
    if (not month or not year or month < 1 or month > 12 or
            year < 1 or year > 99):
        messagebox.showinfo(
            title=Titles.WARN_TITLE.value,
            message=InfoTexts.WRONG_INPUT.value
        )
        return True


def date_validate(day, month, year):
    days = calendar.TextCalendar(firstweekday=0).formatmonth(
        int('20' + year), int(month)
    )
    if day not in days:
        messagebox.showinfo(
            title=Titles.WARN_TITLE.value,
            message=InfoTexts.WRONG_INPUT.value
        )
        return True


def int_validate(value):
    try:
        if not value:
            raise TypeError
        value = int(value)
        if value < 0:
            raise TypeError
    except Exception:
        messagebox.showinfo(
            title=Titles.WARN_TITLE.value,
            message=InfoTexts.WRONG_INPUT.value
        )
        return True


def float_validate(value):
    try:
        if not value:
            raise TypeError
        value = float(value)
        if value < 0:
            raise TypeError
    except Exception:
        messagebox.showinfo(
            title=Titles.WARN_TITLE.value,
            message=InfoTexts.WRONG_INPUT.value
        )
        return True


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def create_sales_month_data(month, year, stock):
    ''' если месяц еще не рассматривался при продажах,
        создаем запись данного месяца '''
    if month_year_validate(1, year):
        return
    if not stock:
        return
    with sqlite3.connect(resource_path('gui.db')) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(''' INSERT INTO sales (month, year,
                           photo_sold, video_sold, amount_sold, stock)
                           VALUES (:month, :year, :photo_sold, :video_sold,
                           :amount_sold, :stock) ''',
                           {
                                'month': month, 'year': year, 'photo_sold': 0,
                                'video_sold': 0, 'amount_sold': 0,
                                'stock': stock
                            })
            conn.commit()
        except Exception:
            messagebox.showinfo(
                title=Titles.WARN_TITLE.value,
                message=InfoTexts.ERROR_TEXT.value
            )
            return


def create_month_data(month, year):
    ''' если месяц еще не рассматривался, создаем дни данного месяца '''
    dates = calendar.monthcalendar(year=int('20' + str(year)),
                                   month=int(month))
    days = [(date, month, year, 0, 0)
            for week in dates for date in week]
    with sqlite3.connect(resource_path('gui.db')) as conn:
        cursor = conn.cursor()
        insert_line = ''' INSERT INTO loads (day, month, year,
                      photo_load, video_load) VALUES (?, ?, ?, ?, ?); '''
        try:
            cursor.executemany(insert_line, days)
            conn.commit()
        except Exception:
            messagebox.showinfo(
                title=Titles.WARN_TITLE.value,
                message=InfoTexts.ERROR_TEXT.value
            )
            return
    return days
