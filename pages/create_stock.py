import sqlite3
from tkinter import Button, Entry, Label, messagebox
from src.helper import clear_frame, resource_path
from src.global_enums.literals import (
    Titles, InfoTexts, LabelTexts, ButtonTexts
)
from configure import DB_NAME


def create_stock(frame):
    ''' создать сток '''
    clear_frame(frame)
    Label(frame, text=LabelTexts.CREATE_STOCK.value).grid(
        row=0, column=0, columnspan=2
    )
    Label(frame, text=LabelTexts.STOCK.value).grid(row=1, column=0)
    stock_name = Entry(frame, width=25)
    stock_name.grid(row=1, column=1)
    Button(
        frame, text=ButtonTexts.CREATE.value,
        command=lambda: save_stock(stock_name.get())
    ).grid(row=2, column=0, columnspan=2)


def save_stock(stock_name):
    if not stock_name:
        messagebox.showinfo(
            title=Titles.WARN_TITLE.value,
            message=InfoTexts.NAME_STOCK.value
        )
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            stock = cursor.execute(''' SELECT stock FROM stocks WHERE
                                   stock=:stock ''',
                                   {'stock': stock_name}).fetchone()
            if stock:
                messagebox.showinfo(
                    title=Titles.WARN_TITLE.value,
                    message=InfoTexts.DUPLICATE.value
                )
                return
            cursor.execute('INSERT INTO stocks VALUES (:stock)',
                           {
                                'stock': stock_name
                            })
            conn.commit()
    except Exception:
        messagebox.showinfo(
            title=Titles.WARN_TITLE.value,
            message=InfoTexts.ERROR_TEXT.value
        )
        return
    messagebox.showinfo(
            title=Titles.SUCCESS_TITLE.value,
            message=InfoTexts.STOCK_CREATED.value
        )
