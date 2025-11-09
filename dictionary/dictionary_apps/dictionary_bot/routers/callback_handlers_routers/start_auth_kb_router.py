from aiogram import F, Router, types
from aiogram.types import CallbackQuery
from dictionary.dictionary_apps.dictionary_bot.keyboards.kb_auth_reg import RegDataAction, RegData


router = Router(name='reg_auth')

# Test callback
# @router.callback_query()
# async def debug_all_callbacks(callback_query: CallbackQuery):
#     print("RAW CALLBACK:", callback_query.data)
#     await callback_query.answer()

@router.callback_query(
    RegData.filter(F.action == RegDataAction.reg),
                       )
async def start_reg(callback_query: CallbackQuery):
    print("REG")
    await callback_query.message.answer(
        text=f"Введите ник:",
        reply_markup=types.ReplyKeyboardRemove()
    )

@router.callback_query(RegData.filter(F.action == RegDataAction.auth))
async def start_auth(callback_query: CallbackQuery):

    print("AUTH", callback_query.answer(text='auth'))
    await callback_query.answer(
        text="Введите пароль:",
        reply_markup=types.ReplyKeyboardRemove()
    )


@router.callback_query(RegData.filter(F.action == RegDataAction.cancel))
async def start_cancel(callback_query: CallbackQuery):
    print("CANCEL")
    await callback_query.answer(
        text="Введите пароль:",
        reply_markup=types.ReplyKeyboardRemove()
    )
