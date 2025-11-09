from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.utils import markdown
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from pathlib import Path

from dictionary.dictionary_apps.dictionary_bot.db import BotDBClass
#from estate_agency.estate_bot.base_name import BotDB

from dictionary.dictionary_apps.dictionary_bot.keyboards.kb_auth_reg import build_auth_reg_kb
from dictionary.config.env import BASE_DIR

router = Router(name=__name__)
class OrderRegister(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()
    waiting_for_check_password = State()

#BotDB = BotDBClass(Path('C:/Python311/django/dictionary/dictionary/db_words.sqlite3'))
BotDB = BotDBClass(Path(BASE_DIR)/ 'db_words.sqlite3')

@router.message(CommandStart())
#@router.callback_query()
async def start(message, state: FSMContext):
    await message.bot.send_message(message.from_user.id, f'Hi - {BotDB}')

    if (not BotDB.user_exists(message.from_user.id)):
        print('HANDLERS_START')
        await message.answer(
            text=f"Добро пожаловать, {markdown.hbold(message.from_user.first_name)} Выберите действие в меню!",
            parse_mode=ParseMode.HTML,
            reply_markup=build_auth_reg_kb(),
        )

    else:
        print('Y')
        await message.answer("Введите пароль:", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(OrderRegister.waiting_for_check_password)