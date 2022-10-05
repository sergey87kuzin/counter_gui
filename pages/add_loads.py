import sqlite3
from datetime import date
from tkinter import (
    Button, Entry, Label, W, messagebox
)
from .helper import (
    clear_frame, date_insert, registrate_inputs, month_year_validate,
    date_validate, int_validate, resource_path, create_month_data
)
from src.global_enums.literals import (
    Titles, InfoTexts, LabelTexts, ButtonTexts
)


def add_loads(frame):
    ''' вносим данные по загрузкам '''
    clear_frame(frame)
    loads_title = Label(frame, text=LabelTexts.LOADS.value)
    loads_title.grid(row=0, column=0, columnspan=2)
    today = str(date.today())
    curr_date = today[8:10]
    Label(frame, text=LabelTexts.DATE.value).grid(
        row=1, column=0, sticky=W
    )
    date_input = Entry(frame, width=2)
    date_input.insert(0, curr_date)
    date_input.grid(row=1, column=1, sticky=W)
    month_input, year_input = date_insert(frame)
    photo_text = Label(frame, text=LabelTexts.PHOTO.value)
    video_text = Label(frame, text=LabelTexts.VIDEO.value)
    photo_input = Entry(frame, width=3)
    photo_input.insert(0, 0)
    video_input = Entry(frame, width=3)
    video_input.insert(0, 0)
    texts = (photo_text, video_text)
    entries = (photo_input, video_input)
    registrate_inputs(texts, entries, 4)
    Button(
        frame, text=ButtonTexts.SAVE.value, command=lambda: save_loads(
            date_input.get(), month_input.get(), year_input.get(),
            photo_input.get(), video_input.get()
        )
    ).grid(row=6, column=0, columnspan=2)


def save_loads(day, month, year, photo, video):
    ''' сохранение внесенных данных о загрузках '''
    if month_year_validate(month, year):
        return
    if date_validate(day, month, year):
        return
    if int_validate(photo) or int_validate(video):
        return
    with sqlite3.connect(resource_path('gui.db')) as conn:
        cursor = conn.cursor()
        try:
            day_line = cursor.execute(
                ''' SELECT day, month, year, photo_load, video_load
                FROM loads WHERE day=:date AND month=:month
                AND year=:year ''',
                {'date': day, 'month': month, 'year': year}
            ).fetchone()
            if not day_line:
                days = create_month_data(month, year)
                if not days:
                    return
            cursor.execute('''UPDATE loads SET
                            photo_load = :photo,
                            video_load = :video
                            WHERE day = :day AND
                                  month = :month AND
                                  year = :year''', {
                                'photo': int(photo) + int(day_line[3]),
                                'video': int(video) + int(day_line[4]),
                                'day': day,
                                'month': month,
                                'year': year
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
                message=InfoTexts.SUCCESS_TEXT.value
            )