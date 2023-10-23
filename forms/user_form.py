from aiogram.fsm.state import State, StatesGroup


class RegistrationForm(StatesGroup):
    username = State()
    mail = State()
