from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from database.db import session
from database.models import Student
from keyboards.inline import get_register_button
from keyboards.reply import get_main_menu_keyboard

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    """
    Обрабатывает команду /start, проверяя регистрацию пользователя в базе данных.
    Если пользователь уже зарегистрирован, приветствует его и показывает главное меню.
    В противном случае предлагает зарегистрироваться, отправляя клавиатуру для регистрации.
    """

    student = session.query(Student).filter_by(id=message.from_user.id).first()
    if student:
        await message.answer(
            f"Привет, {student.first_name}!\n\nДоступные команды:\n\n"
            "/enter_scores - Ввести баллы по ЕГЭ\n"
            "/view_scores - Просмотреть свои баллы по ЕГЭ\n"
            "/help - Показать справку",
            reply_markup=get_main_menu_keyboard(),
        )
    else:
        await message.answer(
            "Привет! Я помогу тебе зарегистрироваться и добавить твои баллы ЕГЭ.\n\n"
            "Нажми кнопку ниже для регистрации.",
            reply_markup=get_register_button(),
        )
