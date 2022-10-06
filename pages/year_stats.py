import sqlite3
from datetime import date
from tkmacosx import CircleButton
from tkinter import (
    Button, Entry, Label, W, N, LabelFrame, messagebox
)
from src.helper import (
    clear_frame, resource_path, create_month_data
)
from src.validators import month_year_validate
from src.global_enums.literals import (
    Titles, InfoTexts, LabelTexts, ButtonTexts
)
from src.global_enums.colours import ElementColour
from configure import DB_NAME


def year_stats(frame):
    ''' позволяет указать, статистику загрузок какого года показать '''
    clear_frame(frame)
    Label(frame, text=LabelTexts.YEAR_STATS.value).grid(
        row=0, column=0, columnspan=2
    )
    today = str(date.today())
    curr_year = today[2:4]
    Label(frame, text=LabelTexts.YEAR.value).grid(
        row=1, column=0, sticky=W
    )
    year_input = Entry(frame, width=2)
    year_input.insert(0, curr_year)
    year_input.grid(row=1, column=1, sticky=W)
    Button(
        frame, text=ButtonTexts.SHOW_STATS.value,
        command=lambda: show_year_loads(frame, year_input.get())
    ).grid(row=4, column=0, columnspan=2)


def show_year_loads(frame, year):
    if month_year_validate(1, year):
        return
    clear_frame(frame)
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            results = cursor.execute(
                ''' SELECT day, month, year, photo_load, video_load
                    FROM loads WHERE year=:year ''',
                {'year': year}).fetchall()
    except Exception:
        messagebox.showinfo(
            title=Titles.WARN_TITLE.value,
            message=InfoTexts.ERROR_TEXT.value
        )
        return
    month_results = {}
    for line in results:
        if int(line[1]) in month_results:
            month_results[int(line[1])].append(line)
        else:
            month_results[int(line[1])] = [line, ]
    for i in range(1, 13):
        if i not in month_results:
            month_data = create_month_data(i, year)
            if not month_data:
                return
        else:
            month_data = month_results[i]
        month_frame = LabelFrame(frame, text=str(i))
        month_frame.grid(row=(i - 1) // 4, column=(i - 1) % 4, sticky=N)
        for ind, day_data in enumerate(month_data):
            day_frame = LabelFrame(month_frame)
            day_frame.grid(row=ind // 7, column=ind % 7, sticky=N)
            day_for_year_stats(day_frame, day_data)


def day_for_year_stats(frame, line):
    ''' форма дня для общего календаря на год '''
    if line[0] != 0:
        Label(frame, text=str(line[0]), width=2).grid(
            row=0, column=0, columnspan=2
        )
        if line[3] != 0:
            CircleButton(
                frame, text='',
                bg=ElementColour.PHOTO_CIRCLE.value, radius=5
            ).grid(row=1, column=0)
        if line[4] != 0:
            CircleButton(
                frame, text='',
                bg=ElementColour.VIDEO_CIRCLE.value, radius=5
            ).grid(row=1, column=1)
