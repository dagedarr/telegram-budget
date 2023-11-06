from aiogram.fsm.state import State, StatesGroup


class CategoryForm(StatesGroup):
    title = State()


class CategoryUpdateForm(StatesGroup):
    old_title = State()
    new_title = State()


class AliasForm(StatesGroup):
    title = State()
