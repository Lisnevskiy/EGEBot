from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command(commands=["help"]))
async def help(message: Message):
    """
    Обработчик команды /help для вывода справки по доступным командам бота.
    Отправляет пользователю список доступных команд и их описания.
    """

    help_text = (
        "Доступные команды:\n\n"
        "/register - Зарегистрироваться в списке учеников\n"
        "/enter_scores - Ввести баллы по ЕГЭ\n"
        "/view_scores - Просмотреть свои баллы по ЕГЭ\n"
        "/help - Показать справку"
    )
    await message.answer(help_text)


@router.message(F.text == "❓ Помощь")
async def help_button_handler(message: Message):
    """Обработчик нажатия кнопки "❓ Помощь", которая выполняет функцию команды /help"""

    await help(message)
