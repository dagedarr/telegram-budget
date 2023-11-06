from aiogram.filters.callback_data import CallbackData


class CategoryDetailsCallbackData(
    CallbackData, prefix='cat_det'
):
    category_id: int


class CategoryActionsCallbackData(
    CallbackData,
    prefix='cat_act'
):
    action: str
    category_id: int
