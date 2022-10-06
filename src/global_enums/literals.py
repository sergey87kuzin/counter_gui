from enum import Enum


class Choices(Enum):
    GRAPHICS = ('Год суммарно', 'Месяц по стокам')


class Titles(Enum):
    ROOT_TITLE = 'Счетчик для стоков'
    RESULT_TITLE = 'Результат'
    FRAME_TITLE = 'Ваши данные'
    QUIT_TITLE = 'Выход'
    WARN_TITLE = 'Внимание'
    SUCCESS_TITLE = 'Ура'
    GRAPHIC_TITLE = 'Результат Вашей работы наглядно'


class InfoTexts(Enum):
    QUIT_TEXT = 'Хотите выйти?'
    WARN_STOCK_TEXT = '''Не указано ни одного стока, пожалуйста, задайте
                      сток в соответствующем разделе'''
    WARN_NO_STOCK = 'Выберите сток'
    ERROR_TEXT = 'что-то пошло не так('
    SUCCESS_TEXT = 'запись добавлена'
    NAME_STOCK = 'назовите сток'
    DUPLICATE = 'Такой сток уже существует'
    STOCK_CREATED = 'Сток создан'
    CHOOSE_GRAPH = 'выберите тип графика'
    NO_YEAR_DATA = 'вы не вносили данных по продажам этого года'
    NO_MONTH_DATA = 'вы не вносили данных по продажам этого месяца'
    WRONG_INPUT = 'некорректно внесено значение'
    WRONG_TYPE = 'нужно вносить цифры'


class ButtonTexts(Enum):
    ADD_LOADS = 'Добавить загрузки'
    MONTH_STATS = 'Посмотреть данные месяца'
    YEAR_STATS = 'Посмотреть данные года'
    ADD_INCOME = 'Внести доходы'
    CREATE_STOCK = 'Создать сток'
    GRAPHIC = 'График'
    TOTAL = 'Суммарный итог'
    ADD = 'Внести'
    SAVE = 'сохранить'
    CREATE = 'создать'
    PLOT = 'Построить'
    SHOW = 'Показать'
    SHOW_STATS = 'Показать статистику'


class LabelTexts(Enum):
    SALES = 'Продажи'
    LOADS = 'Загрузки'
    PHOTO = 'фотографии'
    VIDEO = 'видео'
    INCOME = 'доход'
    STOCK = 'сток'
    DATE = 'Дата'
    MONTH = 'Месяц'
    YEAR = 'год'
    CREATE_STOCK = 'Создайте сток'
    GRAPHIC_TYPE = 'вид графика'
    MONTH_STATS = 'Статистика месяца'
    YEAR_STATS = 'Статистика года'
    GRAPHIC_TOP = 'Построение графика'
    TOTAL_TOP = 'Итоговая таблица'


class ErrorMessages(Enum):
    WRONG_BUTTON_COUNT = 'Неверное число кнопок'
    WRONG_BUTTON_NAME = 'Неверное название кнопки'
