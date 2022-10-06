import pytest
from stock_counter import StockCounter


@pytest.fixture
def tk_work():
    stock = StockCounter()
    yield stock
    stock.root.quit()
    stock.second_screen.quit()
