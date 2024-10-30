from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    """Класс состояния для процесса регистрации пользователя"""

    waiting_for_name = State()
    """Ожидание ввода имени пользователя"""
    waiting_for_surname = State()
    """Ожидание ввода фамилии пользователя"""
