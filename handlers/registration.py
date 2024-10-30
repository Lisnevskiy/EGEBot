from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.db import session
from database.models import Student
from keyboards.reply import get_main_menu_keyboard
from states.registration import Registration

router = Router()


@router.message(Command(commands=["register"]))
async def register(message: Message, state: FSMContext):
    """
    Обрабатывает команду /register, проверяя наличие пользователя в базе данных.
    Если пользователь не зарегистрирован, начинает процесс регистрации,
    переводя FSM в состояние ожидания имени пользователя.
    """

    existing_student = session.query(Student).filter_by(id=message.from_user.id).first()

    if existing_student:
        await message.answer("Ты уже зарегистрирован!")
        return

    # Если идентификатора нет, начинаем регистрацию, запрашивая имя
    await state.set_state(Registration.waiting_for_name)
    await message.answer("Введи свое имя:")


@router.message(Registration.waiting_for_name)
async def get_first_name(message: Message, state: FSMContext):
    """
    Обрабатывает ввод имени пользователя и переводит FSM в состояние ожидания фамилии.
    Сохраняет введенное имя во временные данные состояния
    """

    first_name = message.text.strip()
    await state.update_data(first_name=first_name)
    await message.answer("Введи свою фамилию:")
    await state.set_state(Registration.waiting_for_surname)


@router.message(Registration.waiting_for_surname)
async def get_surname(message: Message, state: FSMContext):
    """
    Обрабатывает ввод фамилии пользователя, завершает регистрацию,
    создавая запись в базе данных, и очищает FSM состояние.
    Создает нового студента с уникальным идентификатором и сохраняет его в базе.
    """

    last_name = message.text.strip()
    data = await state.get_data()
    first_name = data.get("first_name")

    # Создаем нового студента с уникальным идентификатором
    student = Student(id=message.from_user.id, first_name=first_name, last_name=last_name)
    session.add(student)
    session.commit()
    await message.answer(f"Регистрация успешна, {first_name}!", reply_markup=get_main_menu_keyboard())
    await state.clear()


@router.callback_query(F.data == "register")
async def register_button_handler(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает нажатие инлайн-кнопки регистрации"""

    await register(callback.message, state)
    await callback.answer()
