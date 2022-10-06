import sqlite3
from tkmacosx import CircleButton
from tkinter import (
    Button, Label, LabelFrame, messagebox
)
from src.helper import (
    clear_frame, resource_path,
    date_insert, create_month_data
)
from src.validators import month_year_validate
from src.global_enums.literals import (
    Titles, InfoTexts, LabelTexts, ButtonTexts
)
from src.global_enums.colours import ElementColour
from configure import DB_NAME


def month_stats(frame):
    ''' позволяет указать, статистику загрузок какого месяца показать '''
    clear_frame(frame)
    Label(frame, text=LabelTexts.MONTH_STATS.value).grid(
        row=0, column=0, columnspan=2
    )
    month_input, year_input = date_insert(frame)
    Button(
        frame, text=ButtonTexts.SHOW.value,
        command=lambda: show_stats(frame, month_input.get(), year_input.get())
    ).grid(row=4, column=0, columnspan=2)


def show_stats(frame, month, year):
    ''' показывает статистику загрузок выбранного месяца '''
    if month_year_validate(month, year):
        return
    clear_frame(frame)
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            results = cursor.execute(
                ''' SELECT day, month, year, photo_load, video_load
                    FROM loads WHERE month=:month AND year=:year ''',
                {'month': month, 'year': year}).fetchall()
    except Exception:
        messagebox.showinfo(
            title=Titles.WARN_TITLE.value,
            message=InfoTexts.ERROR_TEXT.value
        )
        return True
    if not results:
        results = create_month_data(month, year)
        if not results:
            return
    for ind, result in enumerate(results):
        day_frame = LabelFrame(frame, text=str(result[0]))
        day_frame.grid(row=ind // 7, column=ind % 7)
        day_loads(day_frame, result)


def day_loads(frame, line):
    ''' создание формы дня с данными загрузки '''
    if line[0] != 0:
        CircleButton(
            frame, text=str(line[3]),
            bg=ElementColour.PHOTO_CIRCLE.value, radius=15
        ).grid(row=0, column=0)
        CircleButton(
            frame, text=str(line[4]),
            bg=ElementColour.VIDEO_CIRCLE.value, radius=15
        ).grid(row=0, column=1)
