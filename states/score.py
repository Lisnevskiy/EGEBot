from aiogram.fsm.state import State, StatesGroup


class EnterScore(StatesGroup):
    """Класс состояния для процесса ввода баллов по ЕГЭ"""

    subject = State()
    """Ожидание ввода названия предмета"""
    score = State()
    """Ожидание ввода балла за предмет"""
    confirm = State()
    """Подтверждение ввода баллов"""
