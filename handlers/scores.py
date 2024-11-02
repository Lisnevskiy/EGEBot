from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.db import session
from database.models import Score, Student
from keyboards.inline import get_confirmation_keyboard, get_register_button
from keyboards.reply import get_main_menu_keyboard
from states.score import EnterScore

router = Router()


@router.message(Command(commands=["enter_scores"]))
async def enter_scores(message: Message, state: FSMContext):
    """
    Обрабатывает команду /enter_scores и инициирует процесс ввода баллов.
    Проверяет, зарегистрирован ли пользователь в системе. Если зарегистрирован,
    переводит FSM в состояние ожидания названия предмета для ввода баллов.
    """

    student = session.query(Student).filter_by(id=message.from_user.id).first()
    if not student:
        await message.answer(
            "Тебя еще нет в списке пользователей. Используй команду /register для регистрации.",
            reply_markup=get_register_button(),
        )
        return

    await message.answer("Введи название предмета:")
    await state.set_state(EnterScore.subject)


@router.message(EnterScore.subject)
async def get_subject(message: Message, state: FSMContext):
    """
    Обрабатывает ввод названия предмета и переводит FSM в состояние ожидания баллов.
    Сохраняет введенное название предмета во временные данные состояния.
    """

    subject = message.text.strip()
    await state.update_data(subject=subject)
    await message.answer(f"Теперь введи балл по предмету {subject}:")
    await state.set_state(EnterScore.score)


@router.message(EnterScore.score)
async def get_score(message: Message, state: FSMContext):
    """
    Обрабатывает ввод баллов и сохраняет или обновляет информацию в базе данных.
    Проверяет корректность введенных данных, обновляет существующую запись или создает новую,
    после чего предлагает пользователю ввести баллы по другому предмету или завершить ввод.
    """

    try:
        score = int(message.text.strip())
        if not 0 <= score <= 100:
            raise ValueError
    except ValueError:
        await message.answer("Пожалуйста, введи корректный балл (целое число от 0 до 100).")

    data = await state.get_data()
    subject = data.get("subject")

    student = session.query(Student).filter_by(id=message.from_user.id).first()

    existing_score = session.query(Score).filter_by(student_id=student.id, subject=subject).first()

    if existing_score:
        existing_score.score = score
        action_text = "обновлены"
    else:
        score_entry = Score(subject=subject, score=score, student_id=student.id)
        session.add(score_entry)
        action_text = "сохранены"

    session.commit()
    await message.answer(
        f"Баллы по предмету {subject} успешно {action_text}!\n\n" "Хочешь добавить еще один предмет?",
        reply_markup=get_confirmation_keyboard(),
    )
    await state.set_state(EnterScore.confirm)


@router.message(Command(commands=["view_scores"]))
async def view_scores(message: Message):
    """
    Обрабатывает команду /view_scores и отображает сохраненные баллы пользователя.
    Проверяет, зарегистрирован ли пользователь и есть ли у него сохраненные баллы,
    затем отображает каждый предмет и сумму баллов.
    """

    student = session.query(Student).filter_by(id=message.from_user.id).first()
    if not student:
        await message.answer(
            "Тебя еще нет в списке пользователей. Используй команду /register для регистрации.",
            reply_markup=get_register_button(),
        )
        return

    scores = session.query(Score).filter_by(student_id=student.id).all()
    if not scores:
        await message.answer(
            "У тебя пока нет сохраненных баллов по ЕГЭ. Используй команду /enter_scores чтобы добавить баллы.",
        )
        return

    # Формируем красивый вывод баллов
    total_score = 0
    response = f"📊 Твои баллы по ЕГЭ, {student.first_name}:\n\n"

    for score in scores:
        total_score += score.score
        response += f"📝 {score.subject}: {score.score} баллов\n"

    response += f"\n📈 Общая сумма баллов: {total_score}"
    # Добавляем среднее значение, если есть хотя бы один предмет
    if scores:
        average_score = total_score / len(scores)
        response += f"\n📊 Средний балл: {average_score:.1f}"

    await message.answer(response, reply_markup=get_main_menu_keyboard())


@router.message(F.text == "📝 Ввести баллы")
async def enter_scores_button_handler(message: Message, state: FSMContext):
    """Обрабатывает нажатие кнопки "📝 Ввести баллы" и вызывает команду /enter_scores"""

    await enter_scores(message, state)


@router.message(F.text == "📊 Посмотреть баллы")
async def view_scores_button_handler(message: Message):
    """Обрабатывает нажатие кнопки "📊 Посмотреть баллы" и вызывает команду /view_scores"""

    await view_scores(message)


@router.callback_query(F.data.startswith("confirm_"))
async def process_confirmation(callback: CallbackQuery, state: FSMContext):
    """
    Обрабатывает выбор пользователя по инлайн-кнопке подтверждения добавления баллов.
    Если пользователь нажимает "Да", переводит FSM в состояние ожидания следующего предмета,
    иначе завершает ввод баллов и очищает FSM состояние.
    """

    action = callback.data.split("_")[1]

    # Удаляем инлайн-кнопки
    await callback.message.edit_reply_markup(reply_markup=None)

    if action == "yes":
        await callback.message.answer("Введи название следующего предмета:")
        await state.set_state(EnterScore.subject)
    else:
        await callback.message.answer(
            "Ввод баллов завершен.\n" "Ты можешь посмотреть все свои баллы по ЕГЭ с помощью команды /view_scores",
            reply_markup=get_main_menu_keyboard(),
        )
        await state.clear()

    await callback.answer()
