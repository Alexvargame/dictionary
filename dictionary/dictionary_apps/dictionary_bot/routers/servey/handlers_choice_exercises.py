from aiogram import Router, F
from aiogram.utils import markdown
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery


#from estate_agency.estate_bot.db import BotDBClass

from dictionary.dictionary_apps.dictionary_bot.keyboards.employee_kb.exercises_kb import( build_exercises_kb,
                                                                                          ExercisesData, ExercisesDataAction)
from dictionary.dictionary_apps.dictionary_bot.keyboards.employee_kb.main_employee_kb import (EmployeeData, EmployeeDataAction,
                                                                                            AdminData, AdminDataAction)
from dictionary.dictionary_apps.dictionary_bot.keyboards.employee_kb.main_employee_kb import build_employee_kb, build_admin_kb

from dictionary.dictionary_apps.dictionary_bot.base_name import BotDB

from .states import OrderExercises

router = Router(name='choice_exercises')

@router.callback_query(AdminData.filter(F.action == AdminDataAction.exercises))
@router.callback_query(EmployeeData.filter(F.action == EmployeeDataAction.exercises))
async def get_exercises_menu_item(clbk: CallbackQuery, state: FSMContext):
    try:
        await clbk.message.delete()  # 💥 удалить сообщение с кнопками
    except Exception as e:
        print(f"Не удалось удалить сообщение: {e}")
    await clbk.message.answer(

        text=f"Выберите упражнение:",
        parse_mode=ParseMode.HTML,
        reply_markup=build_exercises_kb(),
    )
    await state.set_state(OrderExercises.waiting_for_exercise)
