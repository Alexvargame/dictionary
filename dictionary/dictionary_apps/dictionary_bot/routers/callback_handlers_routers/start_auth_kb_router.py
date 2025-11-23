from aiogram import F, Router, types
from aiogram.types import CallbackQuery
from dictionary.dictionary_apps.dictionary_bot.keyboards.kb_auth_reg import RegDataAction, RegData


router = Router(name='reg_auth')

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

    print("AUTH")
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
