import sqlite3
import pytest
from stock_counter import StockCounter
from configure import DB_NAME


@pytest.fixture
def tk_work():
    stock = StockCounter()
    yield stock
    stock.root.quit()
    stock.second_screen.quit()


@pytest.fixture
def input_stocks():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.executemany(
            'INSERT INTO stocks (stock) VALUES (?);',
            [(f'stock_{i}',) for i in range(3)]
        )
        conn.commit()
    yield 5
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM stocks')
        conn.commit()
