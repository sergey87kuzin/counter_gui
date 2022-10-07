import sqlite3
from configure import DB_NAME
from tests.helper import frame_button_click
from src.global_enums.literals import (
    ErrorMessages, ButtonNames, LabelNames
)


def test_create_stock(tk_work):
    ''' Проверка добавления позиции стока по нажатию кнопок '''
    stock = tk_work
    entries = [(LabelNames.STOCK.value, 'some_stock')]
    frame_button_click(stock, entries, ButtonNames.STOCK.value)

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            result = cursor.execute(
                ' SELECT stock FROM stocks'
            ).fetchone()
            assert result[0] == 'some_stock', (
                ErrorMessages.WRONG_STOCK_INPUT.value
            )
    finally:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM stocks')
            conn.commit()
