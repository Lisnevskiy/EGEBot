from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_confirmation_keyboard():
    """Создает и возвращает инлайн-клавиатуру для подтверждения выбора"""

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да", callback_data="confirm_yes"),
                InlineKeyboardButton(text="❌ Нет", callback_data="confirm_no"),
            ]
        ]
    )
    return keyboard


def get_register_button():
    """Создает и возвращает инлайн-клавиатуру с кнопкой для регистрации"""

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Зарегистрироваться", callback_data="register")]]
    )
    return keyboard
