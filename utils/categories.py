from aiogram.filters.callback_data import CallbackData


class CategoryDetailsCallbackData(
    CallbackData, prefix='category'
):
    category_id: int


class CategoryActionsCallbackData(
    CallbackData,
    prefix='category'
):
    action: str
    category_id: int


class AliasDetailsCallbackData(
    CallbackData, prefix='alias'
):
    alias_id: int
    category_id: int


class AliasesActionsCallbackData(
    CallbackData,
    prefix='alias'
):
    action: str
    category_id: int
    alias_id: int


class AliasesCategoryCallbackData(
    CallbackData,
    prefix='alias'
):
    action: str
    category_id: int
