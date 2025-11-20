from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils import markdown
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from asgiref.sync import sync_to_async


#from estate_agency.estate_bot.db import BotDBClass

from dictionary.dictionary_apps.dictionary_bot.keyboards.kb_auth_reg import build_auth_reg_kb
from dictionary.dictionary_apps.dictionary_bot.keyboards.employee_kb.main_employee_kb import build_employee_kb, build_admin_kb
from dictionary.dictionary_apps.dictionary_bot.routers.servey.handlers_exercises.statistic import user_last_update
from .states import OrderRegister
from dictionary.dictionary_apps.users.selectors import user_get

@sync_to_async
def get_user_async(user_id):
    return user_get(user_id)

choice_user_role_dict = {
    2: build_employee_kb(),
    1: build_admin_kb(),
}
#BotDB = BotDBClass(Path(__file__).resolve().parent.parent.parent / 'db.sqlite3')

from dictionary.dictionary_apps.dictionary_bot.base_name import BotDB

router = Router(name='start_FCM')

@router.message(Command('start', prefix="!/"))
async def handlers_start_reg_auth(message: types.Message, state: FSMContext):
    if (not BotDB.user_exists(message.from_user.id)):
        print('FCM')
        await message.answer(
            text=f"Добро пожаловать,, {markdown.hbold(message.from_user.first_name)} Выберите действие в меню!",
            parse_mode=ParseMode.HTML,
            reply_markup=build_auth_reg_kb(),
        )
        await state.set_state(OrderRegister.waiting_for_password)
    else:
        print('Y')
        await state.set_state(OrderRegister.waiting_for_check_password)
        await message.answer("Введите пароль:", reply_markup=types.ReplyKeyboardRemove())


@router.message(OrderRegister.waiting_for_check_password)
async def check_password(message: types.Message, state: FSMContext):
    await state.update_data(name=BotDB.get_username_user(message.from_user.id))
    await state.set_state(OrderRegister.waiting_for_check_password.state)
    await state.update_data(password=message.text)
    data = await state.get_data()
    user_profile = BotDB.get_user_profile(BotDB.get_user_id(message.from_user.id))
    user = await get_user_async(BotDB.get_user_id(message.from_user.id))
    if user_profile[19] == message.from_user.id and user_profile[14] == message.text:
        try:
            await clbk.message.delete()  # 💥 удалить сообщение с кнопками
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")
        await user_last_update(user)
        await message.bot.send_message(message.from_user.id,
                                       f"Добро пожаловать, {message.from_user.first_name}. Выберите действие в меню",
                                       reply_markup=choice_user_role_dict[user_profile[15]])
                                       #build_employee_kb())
    else:
        await message.bot.send_message(message.from_user.id, "Проверьте правильность пароля")
        return
    await state.clear()