import sqlite3
import matplotlib
import matplotlib.pyplot as plt
from tkinter import (
    Button, Label, messagebox, ttk
)
from src.helper import clear_frame, resource_path, date_insert
from src.global_enums.literals import (
    Choices, Titles, InfoTexts, LabelTexts, ButtonTexts, ButtonNames
)
from configure import DB_NAME
matplotlib.use('TkAgg')


def graphic(frame):
    ''' задать параметры графика '''
    clear_frame(frame)
    graphic_title = Label(frame, text=LabelTexts.GRAPHIC_TOP.value)
    graphic_title.grid(row=0, column=0, columnspan=2)
    month_input, year_input = date_insert(frame, 'graphic')
    Label(frame, text=LabelTexts.GRAPHIC_TYPE.value).grid(
        row=4, column=0
    )
    graphic_type = ttk.Combobox(frame, values=Choices.GRAPHICS.value)
    graphic_type.grid(row=4, column=1)
    Button(
        frame, text=ButtonTexts.PLOT.value,
        command=lambda: create_graphic(
            month_input.get(), year_input.get(), graphic_type.get()
        ), name=ButtonNames.GRAPHIC.value
    ).grid(row=5, column=0, columnspan=2)


def create_graphic(month, year, graphic_type):
    ''' Построение графиков '''
    try:
        with sqlite3.connect(resource_path(DB_NAME)) as conn:
            cursor = conn.cursor()
            if graphic_type == Choices.GRAPHICS.value[0]:
                data = cursor.execute(
                    ''' SELECT month, sum(photo_sold), sum(video_sold),
                    sum(amount_sold) FROM sales WHERE year=:year
                    GROUP BY month ''',
                    {'year': year}
                ).fetchall()
                if not data:
                    messagebox.showinfo(
                        title=Titles.WARN_TITLE.value,
                        message=InfoTexts.NO_YEAR_DATA.value
                    )
                    return
                print_graphic(data)
            elif graphic_type == Choices.GRAPHICS.value[1]:
                data = cursor.execute(
                    ''' SELECT stock, sum(photo_sold), sum(video_sold),
                    sum(amount_sold) FROM sales WHERE month=:month
                    AND year=:year GROUP BY stock ''',
                    {'month': month, 'year': year}
                ).fetchall()
                if not data:
                    messagebox.showinfo(
                        title=Titles.WARN_TITLE.value,
                        message=InfoTexts.NO_MONTH_DATA.value
                    )
                    return
                print_graphic(data)
            else:
                messagebox.showinfo(
                    title=Titles.WARN_TITLE.value,
                    message=InfoTexts.CHOOSE_GRAPH.value
                )
                return
    except Exception:
        messagebox.showinfo(
            title=Titles.WARN_TITLE.value,
            message=InfoTexts.ERROR_TEXT.value
        )
        return


def print_graphic(data):
    ''' формирует столбчатые диаграмы на основе данных из БД '''
    label_list = [line[0] for line in data]
    photo_list = [line[1] for line in data]
    video_list = [line[2] for line in data]
    income_list = [line[3] for line in data]
    plt.figure(Titles.GRAPHIC_TITLE.value)
    plt.subplots_adjust(wspace=0.3, hspace=0.5)
    plt.subplot(311)
    plt.bar(label_list, photo_list)
    annotate_bars(label_list, photo_list)
    plt.ylabel(LabelTexts.PHOTO.value)
    plt.subplot(312)
    plt.bar(label_list, video_list)
    annotate_bars(label_list, video_list)
    plt.ylabel(LabelTexts.VIDEO.value)
    plt.subplot(313)
    plt.bar(label_list, income_list)
    annotate_bars(label_list, income_list)
    plt.ylabel(LabelTexts.INCOME.value)
    plt.show()


def annotate_bars(label_list, data_list):
    ''' подписывает столбцы диаграм '''
    plt.xticks(ticks=label_list, labels=label_list, rotation=45)
    for i in range(len(data_list)):
        plt.annotate(
            str(data_list[i]), xy=(label_list[i], data_list[i]),
            ha='center', va='bottom'
        )
