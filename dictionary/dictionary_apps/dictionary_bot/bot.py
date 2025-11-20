import asyncio
import logging


from dictionary.config.django.base import BOT_TOKEN_2, CHAT_ID
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from dictionary.dictionary_apps.dictionary_bot.routers import router as main_router

logger = logging.getLogger(__name__)

class OrderRegister(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()
    waiting_for_check_password = State()

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать работу"),
        BotCommand(command="/cancel", description="Отмена"),
    ]
    await bot.set_my_commands(commands)

async def main():

    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    # Объявление и инициализация объектов бота и диспетчера
    print('TOKEN', type(BOT_TOKEN_2))
    bot = Bot(token=BOT_TOKEN_2)#, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(main_router)

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
