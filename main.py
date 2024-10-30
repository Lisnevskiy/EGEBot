import logging

from aiogram import Bot, Dispatcher

from config import TG_BOT_TOKEN
from handlers.help import router as help_router
from handlers.registration import router as registration_router
from handlers.scores import router as scores_router
from handlers.start import router as start_router

# Инициализация бота и диспетчера
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher()

# Подключаем все обработчики
dp.include_router(start_router)
dp.include_router(scores_router)
dp.include_router(help_router)
dp.include_router(registration_router)


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
