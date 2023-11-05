from aiogram.filters.callback_data import CallbackData


class CategoryDetailsCallbackData(
    CallbackData, prefix='cat_details'
):
    category_id: int
    category_title: str


class CategoryActionsCallbackData(
    CallbackData,
    prefix='cat_actions'
):
    action: str
    title: str
