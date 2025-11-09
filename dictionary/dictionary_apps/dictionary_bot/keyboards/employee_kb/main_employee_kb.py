
from enum import Enum
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,)
from aiogram.filters.callback_data import CallbackData


class EmployeeDataAction(Enum):
    exercises = 'exercises'
    user_message = 'user_messages'
    profile = 'profile'
    contacts = 'contacts'
    cancel = 'cancel'

class EmployeeData(CallbackData, prefix='employee'):
    action: EmployeeDataAction

class AdminDataAction(Enum):
    exercises = 'exercises'
    user_message = 'user_messages'
    profile = 'profile'
    contacts = 'contacts'
    users = 'users'
    cancel = 'cancel'

class AdminData(CallbackData, prefix='admin'):
    action: AdminDataAction

class NextCancelDataAction(Enum):
    continue_exercises = 'continue'
    cancel = 'cancel'

class NextCancelData(CallbackData, prefix='next_cancel'):
    action: NextCancelDataAction

class CancelDataAction(Enum):
    cancel = 'cancel'

class CancelData(CallbackData, prefix='cancel'):
    action: CancelDataAction
def build_admin_kb():
    print ('KWYBOARD_ADMIN')

    exercises = InlineKeyboardButton(
        text="📝Упражнения",
        callback_data=AdminData(action=AdminDataAction.exercises).pack()
    )
    user_message = InlineKeyboardButton(
        text="🖼Сообщения ",
        callback_data=AdminData(action=AdminDataAction.user_message).pack()
    )
    profile = InlineKeyboardButton(
        text='Профиль',
        callback_data=AdminData(action=AdminDataAction.profile).pack()
    )
    contacts = InlineKeyboardButton(
        text='Контакты',
        callback_data=AdminData(action=AdminDataAction.contacts).pack()
    )
    users = InlineKeyboardButton(
        text='Пользователи',
        callback_data=AdminData(action=AdminDataAction.users).pack()
    )
    cancel = InlineKeyboardButton(
        text='Отмена',
        callback_data=AdminData(action=AdminDataAction.cancel).pack()

    )

    first_line = [exercises, user_message]
    second_line = [profile, contacts]
    third_line = [users, cancel]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[first_line, second_line, third_line],
    )
    return markup


def build_employee_kb():
    print ('KWYBOARD_EMP')

    exercises= InlineKeyboardButton(
        text="📝Упражнения",
        callback_data=EmployeeData(action=EmployeeDataAction.exercises).pack()
    )
    user_messages = InlineKeyboardButton(
        text="🖼Сообщения ",
        callback_data=EmployeeData(action=EmployeeDataAction.user_message).pack()
    )
    profile = InlineKeyboardButton(
        text='Профиль',
        callback_data=EmployeeData(action=EmployeeDataAction.profile).pack()
    )
    contacts = InlineKeyboardButton(
        text='Контакты',
        callback_data=EmployeeData(action=EmployeeDataAction.contacts).pack()
    )
    cancel = InlineKeyboardButton(
        text='Отмена',
        callback_data=EmployeeData(action=EmployeeDataAction.cancel).pack()

    )

    first_line = [exercises, user_messages]
    second_line = [profile, contacts]
    third_line = [cancel]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[first_line, second_line, third_line],
        # resize_keyboard=True,
        # one_time_keyboard=True,

    )
    return markup

def build_next_cancel_kb():
    print ('KWYBOARD_NEXT_CANCEL')

    continue_exercises = InlineKeyboardButton(
        text="📝Еще раз",
        callback_data=NextCancelData(action=NextCancelDataAction.continue_exercises).pack()
    )
    cancel = InlineKeyboardButton(
        text="🖼Отмена ",
        callback_data=NextCancelData(action=NextCancelDataAction.cancel).pack()
    )


    first_line = [continue_exercises, cancel]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[first_line],
    )
    return markup

def build_cancel_kb():
    print ('KWYBOARD_CANCEL')
    cancel = InlineKeyboardButton(
        text="🖼Отмена ",
        callback_data=CancelData(action=CancelDataAction.cancel).pack()
    )


    first_line = [cancel]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[first_line],
    )
    return markup