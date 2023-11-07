from aiogram.filters.callback_data import CallbackData


class StatisticCallbackData(
    CallbackData, prefix='statistic'
):
    time_interval: str
