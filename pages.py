import sqlite3
import calendar
import locale
import matplotlib
import matplotlib.pyplot as plt
from datetime import date
from tkmacosx import CircleButton
from tkinter import (
    Button, Entry, Label, W, N, LabelFrame, messagebox, ttk
)
matplotlib.use('TkAgg')

GRAPHICS = ['Год суммарно', 'Месяц по стокам']


def add_loads(frame):
    ''' вносим данные по загрузкам '''
    clear_frame(frame)
    loads_title = Label(frame, text='Загрузки')
    loads_title.grid(row=0, column=0, columnspan=2)
    today = str(date.today())
    curr_date = today[8:10]
    Label(frame, text='Дата').grid(row=1, column=0, sticky=W)
    date_input = Entry(frame, width=2)
    date_input.insert(0, curr_date)
    date_input.grid(row=1, column=1, sticky=W)
    month_input, year_input = date_insert(frame)
    photo_text = Label(frame, text='фотографии')
    video_text = Label(frame, text='видео')
    photo_input = Entry(frame, width=3)
    photo_input.insert(0, 0)
    video_input = Entry(frame, width=3)
    video_input.insert(0, 0)
    texts = (photo_text, video_text)
    entries = (photo_input, video_input)
    registrate_inputs(texts, entries, 4)
    Button(
        frame, text='сохранить', command=lambda: save_loads(
            date_input.get(), month_input.get(), year_input.get(),
            photo_input.get(), video_input.get()
        )
    ).grid(row=6, column=0, columnspan=2)


def month_stats(frame):
    ''' позволяет указать, статистику загрузок какого месяца показать '''
    clear_frame(frame)
    Label(frame, text='Статистика месяца').grid(row=0, column=0, columnspan=2)
    month_input, year_input = date_insert(frame)
    Button(
        frame, text='Показать',
        command=lambda: show_stats(frame, month_input.get(), year_input.get())
    ).grid(row=4, column=0, columnspan=2)


def year_stats(frame):
    ''' позволяет указать, статистику загрузок какого года показать '''
    clear_frame(frame)
    Label(frame, text='Статистика года').grid(row=0, column=0, columnspan=2)
    today = str(date.today())
    curr_year = today[2:4]
    Label(frame, text='год').grid(row=1, column=0, sticky=W)
    year_input = Entry(frame, width=2)
    year_input.insert(0, curr_year)
    year_input.grid(row=1, column=1, sticky=W)
    Button(
        frame, text='Показать',
        command=lambda: show_year_loads(frame, year_input.get())
    ).grid(row=4, column=0, columnspan=2)


def add_income(frame):
    ''' внести данные по продажам '''
    with sqlite3.connect('gui.db') as conn:
        cursor = conn.cursor()
        stocks = cursor.execute('SELECT stock FROM stocks').fetchall()
        if not stocks:
            messagebox.showinfo(
                title='Внимание',
                message='''Не указано ни одного стока, пожалуйста, задайте
                           сток в соответствующем разделе'''
            )
            return
    clear_frame(frame)
    stocks = [stock[0] for stock in stocks]
    loads_title = Label(frame, text='Продажи')
    loads_title.grid(row=0, column=0, columnspan=2)
    month_input, year_input = date_insert(frame)
    photo_text = Label(frame, text='фотографии')
    video_text = Label(frame, text='видео')
    income_text = Label(frame, text='доход')
    stock_text = Label(frame, text='сток')
    photo_input = Entry(frame, width=3)
    photo_input.insert(0, 0)
    video_input = Entry(frame, width=3)
    video_input.insert(0, 0)
    income_input = Entry(frame, width=7)
    income_input.insert(0, 0)
    stock_input = ttk.Combobox(frame, values=stocks)
    texts = (photo_text, video_text, income_text, stock_text)
    entries = (photo_input, video_input, income_input, stock_input)
    registrate_inputs(texts, entries, 4)
    Button(
        frame, text='Внести', command=lambda: update_income(
            month_input.get(), year_input.get(),
            photo_input.get(), video_input.get(), income_input.get(),
            stock_input.get()
        )
    ).grid(row=8, column=0, columnspan=2)


def create_stock(frame):
    ''' создать сток '''
    clear_frame(frame)
    Label(frame, text='Создайте сток').grid(row=0, column=0, columnspan=2)
    Label(frame, text='сток').grid(row=1, column=0)
    stock_name = Entry(frame, width=25)
    stock_name.grid(row=1, column=1)
    Button(
        frame, text='создать', command=lambda: save_stock(stock_name.get())
    ).grid(row=2, column=0, columnspan=2)


def graphic(frame):
    ''' задать параметры графика '''
    clear_frame(frame)
    month_input, year_input = date_insert(frame)
    Label(frame, text='вид графика').grid(row=4, column=0)
    graphic_type = ttk.Combobox(frame, values=GRAPHICS)
    graphic_type.grid(row=4, column=1)
    Button(
        frame, text='Построить', command=lambda: create_graphic(
            month_input.get(), year_input.get(), graphic_type.get()
        )
    ).grid(row=5, column=0, columnspan=2)


def total(frame):
    ''' параметры для итоговой таблицы продаж '''
    clear_frame(frame)
    month_input, year_input = date_insert(frame)
    Button(
        frame, text='Показать статистику', command=lambda: show_total(
            frame, month_input.get(), year_input.get()
        )
    ).grid(row=4, column=0, columnspan=2)


def date_insert(frame):
    ''' добавление полей даты '''
    today = str(date.today())
    curr_year = today[2:4]
    curr_month = today[5:7]
    month_text = Label(frame, text='Месяц')
    year_text = Label(frame, text='Год')
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


def clear_frame(frame):
    ''' очистка рамки перед повторным использованием '''
    for widget in frame.winfo_children():
        widget.destroy()


def show_stats(frame, month, year):
    ''' показывает статистику загрузок выбранного месяца '''
    if month_year_validate(month, year):
        return
    clear_frame(frame)
    with sqlite3.connect('gui.db') as conn:
        cursor = conn.cursor()
        try:
            results = cursor.execute(
                ''' SELECT day, month, year, photo_load, video_load
                    FROM loads WHERE month=:month AND year=:year ''',
                {'month': month, 'year': year}).fetchall()
        except Exception:
            messagebox.showinfo(
                title='Упс',
                message='что-то пошло не так('
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
            frame, text=str(line[3]), bg='red', radius=15
        ).grid(row=0, column=0)
        CircleButton(
            frame, text=str(line[4]), bg='yellow', radius=15
        ).grid(row=0, column=1)


def create_month_data(month, year):
    ''' если месяц еще не рассматривался, создаем дни данного месяца '''
    dates = calendar.monthcalendar(year=int('20' + str(year)),
                                   month=int(month))
    days = [(date, month, year, 0, 0)
            for week in dates for date in week]
    with sqlite3.connect('gui.db') as conn:
        cursor = conn.cursor()
        insert_line = ''' INSERT INTO loads (day, month, year,
                      photo_load, video_load) VALUES (?, ?, ?, ?, ?); '''
        try:
            cursor.executemany(insert_line, days)
            conn.commit()
        except Exception:
            messagebox.showinfo(
                title='Упс',
                message='что-то пошло не так('
            )
            return
    return days


def show_year_loads(frame, year):
    if month_year_validate(1, year):
        return
    clear_frame(frame)
    with sqlite3.connect('gui.db') as conn:
        cursor = conn.cursor()
        try:
            results = cursor.execute(
                ''' SELECT day, month, year, photo_load, video_load
                    FROM loads WHERE year=:year ''',
                {'year': year}).fetchall()
        except Exception:
            messagebox.showinfo(
                title='Упс',
                message='что-то пошло не так('
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
                frame, text='', bg='red', radius=5
            ).grid(row=1, column=0)
        if line[4] != 0:
            CircleButton(
                frame, text='', bg='yellow', radius=5
            ).grid(row=1, column=1)


def create_sales_month_data(month, year, stock):
    ''' если месяц еще не рассматривался при продажах,
        создаем запись данного месяца '''
    if month_year_validate(1, year):
        return
    if not stock:
        return
    with sqlite3.connect('gui.db') as conn:
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
                title='Упс',
                message='что-то пошло не так('
            )
            return


def save_loads(day, month, year, photo, video):
    ''' сохранение внесенных данных о загрузках '''
    if month_year_validate(month, year):
        return
    if date_validate(day, month, year):
        return
    if int_validate(photo) or int_validate(video):
        return
    with sqlite3.connect('gui.db') as conn:
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
                title='Упс',
                message='что-то пошло не так('
            )
            return
        messagebox.showinfo(
                title='Ура',
                message='''запись добавлена'''
            )


def save_stock(stock_name):
    if not stock_name:
        messagebox.showinfo(
            title='Упс',
            message='назовите сток'
        )
    with sqlite3.connect('gui.db') as conn:
        cursor = conn.cursor()
        try:
            stock = cursor.execute(''' SELECT stock FROM stocks WHERE
                                   stock=:stock ''',
                                   {'stock': stock_name}).fetchone()
            if stock:
                messagebox.showinfo(
                    title='Внимание',
                    message='''Такой сток уже существует'''
                )
                return
            cursor.execute('INSERT INTO stocks VALUES (:stock)',
                           {
                                'stock': stock_name
                            })
            conn.commit()
        except Exception:
            messagebox.showinfo(
                title='Упс',
                message='что-то пошло не так('
            )
            return
        messagebox.showinfo(
                title='Ура',
                message='''Сток создан'''
            )


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
            title='Упс',
            message='выберите сток'
        )
        return
    with sqlite3.connect('gui.db') as conn:
        cursor = conn.cursor()
        try:
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
                title='Упс',
                message='что-то пошло не так('
            )
            return
        messagebox.showinfo(
                title='Ура',
                message='''запись добавлена'''
            )


def create_graphic(month, year, graphic_type):
    ''' Построение графиков '''
    with sqlite3.connect('gui.db') as conn:
        cursor = conn.cursor()
        if graphic_type == GRAPHICS[0]:
            try:
                data = cursor.execute(
                    ''' SELECT month, sum(photo_sold), sum(video_sold),
                    sum(amount_sold) FROM sales WHERE year=:year
                    GROUP BY month ''',
                    {'year': year}
                ).fetchall()
            except Exception:
                messagebox.showinfo(
                    title='Упс',
                    message='выберите тип графика'
                )
                return
            if not data:
                messagebox.showinfo(
                    title='Упс',
                    message='''вы не вносили данных по продажам этого года'''
                )
                return
            print_graphic(data)
        elif graphic_type == GRAPHICS[1]:
            try:
                data = cursor.execute(
                    ''' SELECT stock, sum(photo_sold), sum(video_sold),
                    sum(amount_sold) FROM sales WHERE month=:month
                    AND year=:year GROUP BY stock ''',
                    {'month': month, 'year': year}
                ).fetchall()
            except Exception:
                messagebox.showinfo(
                    title='Упс',
                    message='выберите тип графика'
                )
                return
            if not data:
                messagebox.showinfo(
                    title='Упс',
                    message='вы не вносили данных по продажам этого месяца'
                )
                return
            print_graphic(data)
        else:
            messagebox.showinfo(
                title='Упс',
                message='выберите тип графика'
            )
            return


def print_graphic(data):
    ''' формирует столбчатые диаграмы на основе данных из БД '''
    label_list = [line[0] for line in data]
    photo_list = [line[1] for line in data]
    video_list = [line[2] for line in data]
    income_list = [line[3] for line in data]
    plt.figure('Результат Вашей работы наглядно')
    plt.subplots_adjust(wspace=0.3, hspace=0.5)
    plt.subplot(311)
    plt.bar(label_list, photo_list)
    annotate_bars(label_list, photo_list)
    plt.ylabel('фото')
    plt.subplot(312)
    plt.bar(label_list, video_list)
    annotate_bars(label_list, video_list)
    plt.ylabel('видео')
    plt.subplot(313)
    plt.bar(label_list, income_list)
    annotate_bars(label_list, income_list)
    plt.ylabel('доход')
    plt.show()


def annotate_bars(label_list, data_list):
    ''' подписывает столбцы диаграм '''
    plt.xticks(ticks=label_list, labels=label_list, rotation=45)
    for i in range(len(data_list)):
        plt.annotate(
            str(data_list[i]), xy=(label_list[i], data_list[i]),
            ha='center', va='bottom'
        )


def show_total(frame, month, year):
    clear_frame(frame)
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    stock_total = {}
    month_total = {}
    with sqlite3.connect('gui.db') as conn:
        cursor = conn.cursor()
        # data = cursor.execute(
        #         ''' SELECT stock, sum(photo_sold), sum(video_sold),
        #         sum(amount_sold) FROM sales WHERE month=:month
        #         AND year=:year GROUP BY stock ''',
        #         {'month': month, 'year': year}
        #     ).fetchall()
        # if not data:
        #     messagebox.showinfo(
        #         title='Упс',
        #         message='''вы не вносили данных по продажам этого месяца'''
        #     )
        #     return
        # Label(frame, text='сток').grid(row=0, column=0)
        # Label(frame, text='фото').grid(row=0, column=1)
        # Label(frame, text='видео').grid(row=0, column=2)
        # Label(frame, text='доход').grid(row=0, column=3)
        # for ind, line in enumerate(data):
        #     Label(frame, text=line[0]).grid(row=ind + 1, column=0)
        #     Label(frame, text=line[1]).grid(row=ind + 1, column=1)
        #     Label(frame, text=line[2]).grid(row=ind + 1, column=2)
        #     Label(frame, text=line[3]).grid(row=ind + 1, column=3)
        ''' общая таблица за весь год '''
        months = list(calendar.month_abbr)
        try:
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
                title='Упс',
                message='выберите тип графика'
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


def month_year_validate(month, year):
    try:
        month = int(month)
        year = int(year)
    except Exception:
        messagebox.showinfo(
            title='Упс',
            message='нужно вносить цифры'
        )
        return True
    if (not month or not year or month < 1 or month > 12 or
            year < 1 or year > 99):
        messagebox.showinfo(
            title='Упс',
            message='некорректно внесены данные'
        )
        return True


def date_validate(day, month, year):
    days = calendar.TextCalendar(firstweekday=0).formatmonth(
        int('20' + year), int(month)
    )
    if day not in days:
        messagebox.showinfo(
            title='Упс',
            message='некорректно внесена дата'
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
            title='Упс',
            message='некорректно внесено значение'
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
            title='Упс',
            message='некорректно внесено значение'
        )
        return True
