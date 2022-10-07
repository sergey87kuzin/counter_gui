import sqlite3
from configure import DB_NAME
from tests.helper import frame_button_click
from src.global_enums.literals import (
    ErrorMessages, ButtonNames, LabelNames
)


def test_add_load_and_stats(tk_work):
    ''' Проверка добавления позиции загрузки по нажатию кнопок
    и отображения в разделах статистики '''
    stock = tk_work
    entries = [(LabelNames.LOADS_DAY.value, '12'),
               (LabelNames.LOADS_MONTH.value, '11'),
               (LabelNames.LOADS_YEAR.value, '23'),
               (LabelNames.LOADS_PHOTO.value, '111'),
               (LabelNames.LOADS_VIDEO.value, '222')]
    frame_button_click(stock, entries, ButtonNames.ADD_LOADS.value)

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            result = cursor.execute(
                ''' SELECT day, month, year, photo_load, video_load
                FROM loads WHERE day=12 AND month=11 ''').fetchone()
        assert result[0] == 12, ErrorMessages.WRONG_DATE_INPUT.value
        assert result[1] == 11, ErrorMessages.WRONG_MONTH_INPUT.value
        assert result[2] == 23, ErrorMessages.WRONG_YEAR_INPUT.value
        assert result[3] == 111, ErrorMessages.WRONG_PHOTO_INPUT.value
        assert result[4] == 222, ErrorMessages.WRONG_VIDEO_INPUT.value

        ''' после добавления данных о загрузке эта информация должна
        отобразиться в месячном отчете '''
        entries = [(LabelNames.MONTH_MONTH.value, '11'),
                   (LabelNames.MONTH_YEAR.value, '23')]
        frame_button_click(stock, entries, ButtonNames.MONTH.value)
        assert stock.frame.children['day13'].children[
            LabelNames.PHOTO_CIRCLE.value
        ]['text'] == '111', ErrorMessages.WRONG_PHOTO_SHOW.value

        ''' ... и в годовом отчете на карточке даты должна появиться точка '''
        entries = [(LabelNames.YEAR_YEAR.value, '23')]
        frame_button_click(stock, entries, 'year_stats_button')
        assert stock.frame.children[
            'year_stats_month_frame_11'].children[
                'day_frame_13'].children.get(LabelNames.PHOTO_CIRCLE.value), (
            ErrorMessages.WRONG_PHOTO_SHOW.value
        )
    finally:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM loads')
            conn.commit()
