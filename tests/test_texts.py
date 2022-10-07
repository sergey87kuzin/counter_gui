import pytest
from src.global_enums.literals import (
    ErrorMessages, ButtonTexts, LabelTexts
)

CHILD_BUTTONS = (
    ButtonTexts.ADD_LOADS.value, ButtonTexts.ADD_INCOME.value,
    ButtonTexts.MONTH_STATS.value, ButtonTexts.GRAPHIC.value,
    ButtonTexts.YEAR_STATS.value, ButtonTexts.TOTAL.value,
    ButtonTexts.CREATE_STOCK.value
)
ADD_LOADS_LABELS = (
    LabelTexts.LOADS.value, LabelTexts.DATE.value,
    LabelTexts.MONTH.value, LabelTexts.YEAR.value,
    LabelTexts.PHOTO.value, LabelTexts.VIDEO.value
)
MONTH_STATS_LABELS = (
    LabelTexts.MONTH_STATS.value, LabelTexts.MONTH.value,
    LabelTexts.YEAR.value
)
YEAR_STATS_LABELS = (
    LabelTexts.YEAR_STATS.value, LabelTexts.YEAR.value
)
ADD_INCOME_LABELS = (
    LabelTexts.SALES.value, LabelTexts.MONTH.value,
    LabelTexts.YEAR.value, LabelTexts.PHOTO.value,
    LabelTexts.VIDEO.value, LabelTexts.INCOME.value,
    LabelTexts.STOCK.value
)
CREATE_STOCK_LABELS = (
    LabelTexts.CREATE_STOCK.value, LabelTexts.STOCK.value
)
GRAPHIC_LABELS = (
    LabelTexts.GRAPHIC_TOP.value, LabelTexts.MONTH.value,
    LabelTexts.YEAR.value, LabelTexts.GRAPHIC_TYPE.value
)
TOTAL_LABELS = (
    LabelTexts.TOTAL_TOP.value,
    LabelTexts.MONTH.value, LabelTexts.YEAR.value
)


def test_child(tk_work):
    ''' Проверяем, что установленные на стартовом экране
    кнопки правильно подписаны '''
    tk_work.start()
    assert len(tk_work.root.winfo_children()) == len(CHILD_BUTTONS), (
        ErrorMessages.WRONG_BUTTON_COUNT.value
    )
    for child in tk_work.root.winfo_children():
        assert child['text'] in CHILD_BUTTONS, (
            ErrorMessages.WRONG_BUTTON_NAME.value
        )


@pytest.mark.parametrize('root_button, child_button, labels', [
    ('add_loads_button', ButtonTexts.SAVE.value, ADD_LOADS_LABELS),
    ('month_stats_button', ButtonTexts.SHOW.value, MONTH_STATS_LABELS),
    ('year_stats_button', ButtonTexts.SHOW_STATS.value, YEAR_STATS_LABELS),
    ('add_income_button', ButtonTexts.ADD.value, ADD_INCOME_LABELS),
    ('create_stock_button', ButtonTexts.CREATE.value, CREATE_STOCK_LABELS),
    ('graphic_button', ButtonTexts.PLOT.value, GRAPHIC_LABELS),
    ('total_button', ButtonTexts.SHOW_STATS.value, TOTAL_LABELS)
])
def test_labels_buttons_test(
        tk_work, input_stocks, root_button, child_button, labels):
    ''' проверяем, что установленные на экране загрузок
    кнопки и ярлыки подписаны правильно '''
    tk_work.start()
    tk_work.root.children[root_button].invoke()
    for child in tk_work.frame.winfo_children():
        if child.widgetName == 'button':
            assert child['text'] == child_button, (
                ErrorMessages.WRONG_BUTTON_NAME.value
            )
        elif child.widgetName == 'label':
            assert child['text'] in labels, (
                ErrorMessages.WRONG_BUTTON_NAME.value
            )
    assert len(tk_work.frame.winfo_children()) == len(labels) * 2, (
        ErrorMessages.WRONG_BUTTON_COUNT.value
    )
