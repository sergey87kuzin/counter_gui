import sqlite3
import sys
from tkinter import (
    Button, Entry, Label, messagebox, ttk
)
from src.helper import (
    resource_path, clear_frame, date_insert, registrate_inputs,
    create_sales_month_data
)
from src.validators import month_year_validate, int_validate, float_validate
from src.global_enums.literals import (
    Titles, InfoTexts, LabelTexts, ButtonTexts, ButtonNames, LabelNames
)
from configure import DB_NAME


def add_income(frame):
    ''' внести данные по продажам '''
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            stocks = cursor.execute('SELECT stock FROM stocks').fetchall()
            if not stocks:
                messagebox.showinfo(
                    title=Titles.WARN_TITLE.value,
                    message=InfoTexts.WARN_STOCK_TEXT.value
                )
                return
    except Exception as e:
        messagebox.showinfo(
            title=Titles.WARN_TITLE.value,
            message=str(e)
        )
        return

    clear_frame(frame)
    stocks = [stock[0] for stock in stocks]
    loads_title = Label(frame, text=LabelTexts.SALES.value)
    loads_title.grid(row=0, column=0, columnspan=2)
    month_input, year_input = date_insert(frame, 'add_income')
    photo_text = Label(frame, text=LabelTexts.PHOTO.value)
    video_text = Label(frame, text=LabelTexts.VIDEO.value)
    income_text = Label(frame, text=LabelTexts.INCOME.value)
    stock_text = Label(frame, text=LabelTexts.STOCK.value)
    photo_input = Entry(frame, width=3, name=LabelNames.INCOME_PHOTO.value)
    photo_input.insert(0, 0)
    video_input = Entry(frame, width=3, name=LabelNames.INCOME_VIDEO.value)
    video_input.insert(0, 0)
    income_input = Entry(frame, width=7, name=LabelNames.INCOME_INCOME.value)
    income_input.insert(0, 0)
    stock_input = ttk.Combobox(
        frame, values=stocks, name=LabelNames.INCOME_STOCK.value
    )
    texts = (photo_text, video_text, income_text, stock_text)
    entries = (photo_input, video_input, income_input, stock_input)
    registrate_inputs(texts, entries, 4)
    Button(
        frame, text=ButtonTexts.ADD.value, command=lambda: update_income(
            month_input.get(), year_input.get(),
            photo_input.get(), video_input.get(), income_input.get(),
            stock_input.get()
        ), name=ButtonNames.ADD_INCOME.value
    ).grid(row=8, column=0, columnspan=2)


def update_income(
    month, year, photo, video, income, stock
):
    ''' Вносит доходы в БД '''
    if month_year_validate(month, year):
        return
    if (int_validate(photo) or int_validate(video) or
            float_validate(income)):
        return
    if not stock:
        messagebox.showinfo(
            title=Titles.WARN_TITLE.value,
            message=InfoTexts.WARN_NO_STOCK.value
        )
        return
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            record = cursor.execute(
                '''SELECT stock FROM sales WHERE month=:month
                AND year=:year AND stock=:stock''',
                {
                    'month': month, 'year': year, 'stock': stock
                }
            ).fetchone()
            if not record:
                create_sales_month_data(month, year, stock)
            current_line = cursor.execute(
                ''' SELECT month, year, photo_sold, video_sold, amount_sold,
                stock FROM sales WHERE month=:month AND year=:year AND
                stock=:stock ''',
                {
                    'month': month, 'year': year, 'stock': stock
                }
            ).fetchone()
            cursor.execute(
                ''' UPDATE sales SET photo_sold=:photo, video_sold=:video,
                amount_sold=:income WHERE month=:month AND
                year=:year AND stock=:stock ''',
                {
                    'month': month, 'year': year,
                    'photo': int(photo) + int(current_line[2]),
                    'video': int(video) + int(current_line[3]),
                    'income': float(income) + float(current_line[4]),
                    'stock': stock
                })
            conn.commit()
    except Exception:
        messagebox.showinfo(
            title=Titles.WARN_TITLE.value,
            message=InfoTexts.ERROR_TEXT.value
        )
        return
    if 'pytest' not in sys.modules:
        messagebox.showinfo(
                title=Titles.SUCCESS_TITLE.value,
                message=InfoTexts.SUCCESS_TEXT.value
            )
