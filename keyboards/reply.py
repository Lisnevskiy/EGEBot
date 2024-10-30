from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_main_menu_keyboard():
    """Создает и возвращает главное меню с текстовыми кнопками"""

    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="📝 Ввести баллы"),
                KeyboardButton(text="📊 Посмотреть баллы"),
                KeyboardButton(text="❓ Помощь"),
            ]
        ],
    )
    return keyboard
