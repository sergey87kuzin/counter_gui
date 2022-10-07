import sqlite3
from configure import DB_NAME
from tests.helper import frame_button_click
from src.global_enums.literals import (
    ErrorMessages, ButtonNames, LabelNames
)


def test_add_income(tk_work, input_stocks):
    ''' Проверка добавления позиции продаж по нажатию кнопок
    и отображения в разделах статистики '''
    stock = tk_work
    entries = [(LabelNames.INCOME_MONTH.value, '11'),
               (LabelNames.INCOME_YEAR.value, '23'),
               (LabelNames.INCOME_PHOTO.value, '111'),
               (LabelNames.INCOME_VIDEO.value, '222'),
               (LabelNames.INCOME_INCOME.value, '333'),
               (LabelNames.INCOME_STOCK.value, 'stock_1')]
    frame_button_click(stock, entries, ButtonNames.ADD_INCOME.value)

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            result = cursor.execute(
                ''' SELECT month, year, photo_sold, video_sold,
                amount_sold, stock
                FROM sales WHERE month=:month AND year=:year ''',
                {
                    'month': '11', 'year': '23'
                }).fetchone()
            assert result[0] == 11, ErrorMessages.WRONG_MONTH_INPUT.value
            assert result[1] == 23, ErrorMessages.WRONG_YEAR_INPUT.value
            assert result[2] == 111, ErrorMessages.WRONG_PHOTO_INPUT.value
            assert result[3] == 222, ErrorMessages.WRONG_VIDEO_INPUT.value
            assert result[4] == 333, ErrorMessages.WRONG_INCOME_INPUT.value
            assert result[5] == 'stock_1', (
                ErrorMessages.WRONG_STOCK_INPUT.value
            )

        ''' После того, как была внесена информация о продаже, на вкладке
        итоговых результатов за год эта продажа должна отобразиться
        под необходимым стоком в строке нужного месяца '''
        entries = [(LabelNames.TOTAL_MONTH.value, '11'),
                   (LabelNames.TOTAL_YEAR.value, '23')]
        frame_button_click(stock, entries, ButtonNames.TOTAL.value)
        assert stock.frame.children['stock_1_sale_0']['text'] == '333.0', (
            ErrorMessages.WRONG_SALES_SHOW.value
        )
    finally:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM sales')
            conn.commit()
