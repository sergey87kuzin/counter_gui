import sqlite3
import sys
from datetime import date
from tkinter import (
    Button, Entry, Label, W, messagebox
)
from src.helper import (
    clear_frame, date_insert, registrate_inputs, resource_path,
    create_month_data
)
from src.validators import month_year_validate, date_validate, int_validate
from src.global_enums.literals import (
    Titles, InfoTexts, LabelTexts, ButtonTexts, ButtonNames, LabelNames
)
from configure import DB_NAME


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
    date_input = Entry(frame, width=2, name=LabelNames.LOADS_DAY.value)
    date_input.insert(0, curr_date)
    date_input.grid(row=1, column=1, sticky=W)
    month_input, year_input = date_insert(frame, 'add_loads')
    photo_text = Label(frame, text=LabelTexts.PHOTO.value)
    video_text = Label(frame, text=LabelTexts.VIDEO.value)
    photo_input = Entry(frame, width=3, name=LabelNames.LOADS_PHOTO.value)
    photo_input.insert(0, 0)
    video_input = Entry(frame, width=3, name=LabelNames.LOADS_VIDEO.value)
    video_input.insert(0, 0)
    texts = (photo_text, video_text)
    entries = (photo_input, video_input)
    registrate_inputs(texts, entries, 4)
    Button(
        frame, text=ButtonTexts.SAVE.value, command=lambda: save_loads(
            date_input.get(), month_input.get(), year_input.get(),
            photo_input.get(), video_input.get()
        ), name=ButtonNames.ADD_LOADS.value
    ).grid(row=6, column=0, columnspan=2)


def save_loads(day, month, year, photo, video):
    ''' сохранение внесенных данных о загрузках '''
    if month_year_validate(month, year):
        return
    if date_validate(day, month, year):
        return
    if int_validate(photo) or int_validate(video):
        return
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
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
                day_line = (day, month, year, 0, 0)
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
    except Exception as e:
        messagebox.showinfo(
            title=Titles.WARN_TITLE.value,
            message=str(e)
            # message=InfoTexts.ERROR_TEXT.value
        )
        return
    if 'pytest' not in sys.modules:
        messagebox.showinfo(
                title=Titles.SUCCESS_TITLE.value,
                message=InfoTexts.SUCCESS_TEXT.value
            )
