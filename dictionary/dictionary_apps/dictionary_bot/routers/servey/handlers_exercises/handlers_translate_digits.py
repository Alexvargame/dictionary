from asgiref.sync import sync_to_async
import django
import os
import random

from aiogram import Router, F, types
#from aiogram.utils import markdown
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram.filters.callback_data import CallbackData


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dictionary.config.django.base')
django.setup()


from dictionary.dictionary_apps.dictionary_bot.base_name import BotDB


from dictionary.dictionary_apps.dictionary_bot.keyboards.employee_kb.exercises_kb import (ExercisesData, ExercisesDataAction,
                                                                                          build_exercises_kb, build_translate_digits_kb,
                                                                                          create_enum_digit_from_data)
from dictionary.dictionary_apps.words.models import Noun
from dictionary.dictionary_apps.words.repository import NounRepository, WordRepository
from dictionary.dictionary_apps.words.services import NounService, WordService
from dictionary.dictionary_apps.words.selectors import  noun_get
from dictionary.dictionary_apps.users.selectors import user_get
from dictionary.dictionary_apps.dtos.words.request_dto import CreateDigitsExerciseDTO


from ..states import OrderExercisesTranslateDigits
from .statistic import count_score_lifes


router = Router(name='translate_digits')

@sync_to_async
def create_nouns_ids():
    return NounService(NounRepository()).list_objects()

@sync_to_async
def create_words_ids(filters):
    return WordService(WordRepository()).list_objects(filters)
@sync_to_async
def get_noun_for_id(noun_id):
    return noun_get(noun_id)
@sync_to_async
def get_user_async(user_id):
    return user_get(user_id)

units = {
    1: "ein", 2: "zwei", 3: "drei", 4: "vier", 5: "fünf",
    6: "sechs", 7: "sieben", 8: "acht", 9: "neun"
}

teens = {
    10: "zehn", 11: "elf", 12: "zwölf", 13: "dreizehn",
    14: "vierzehn", 15: "fünfzehn", 16: "sechzehn",
    17: "siebzehn", 18: "achtzehn", 19: "neunzehn"
}

tens = {
    20: "zwanzig", 30: "dreißig", 40: "vierzig",
    50: "fünfzig", 60: "sechzig", 70: "siebzig",
    80: "achtzig", 90: "neunzig"
}

def number_to_german(n):
    if n == 0:
        return "null"
    elif n <= 12:
        return {
            1: "eins", 2: "zwei", 3: "drei", 4: "vier",
            5: "fünf", 6: "sechs", 7: "sieben", 8: "acht",
            9: "neun", 10: "zehn", 11: "elf", 12: "zwölf"
        }[n]
    elif 13 <= n <= 19:
        return teens[n]
    elif n < 100:
        unit = n % 10
        ten = n - unit
        if unit == 0:
            return tens[ten]
        return f"{units[unit]}und{tens[ten]}"
    elif 100 <= n < 1000:
        unit = n % 10
        ten = n % 100 - unit
        hundred = n // 100
        print('afwe', unit, ten, hundred)
        if 9 < ten < 20:
            if unit == 0:
                return f"{units[hundred]} hundert {teens[ten]}"
            else:
                return f"{units[hundred]} hundert {teens[ten + unit]}"

        if unit == 0:
            return f"{units[hundred]} hundert {tens[ten]}"
        if ten == 0:
            return f"{units[hundred]} hundert {units[unit]}"
        return f"{units[hundred]} hundert {units[unit]}und{tens[ten]}"
    else:
        return "nicht unterstützt"  # >1000 пока не поддерживаем
async def generate_exercise(digits=[]):
    # Получаем ID лекций из запроса
    exercises = []
    for digit in digits:
        answer = number_to_german(digit)
        exercises.append(
            CreateDigitsExerciseDTO(
                digit=digit,
                correct_answer=answer,
            )
        )
    return exercises

def create_callback_class_for_enum(enum_cls):
    class TranslateDigitsData(CallbackData, prefix='translate_digits'):
        action: enum_cls
    return TranslateDigitsData


@router.callback_query(ExercisesData.filter(F.action == ExercisesDataAction.translate_digits))
async def create_exercises_articles(clbk: CallbackQuery, state: FSMContext):
    print('EXERCISES_TRANSLATE_DIGOTS ')
    limit = 5
    random_numbers = random.sample(range(1, 1001), limit)
    exercises_translate_digits = await generate_exercise(random_numbers)

    print('sel', exercises_translate_digits)
    #await state.update_data(waiting_for_selected_exercises=exercises_translate_digits)

    user = await get_user_async(BotDB.get_user_id(clbk.message.chat.id))
    text_for_user = f"{user.username}  Ваши баллы:{user.score},\n"
    text_for_user += f"  Ваши жизни: {user.lifes} \n\n"
    text_for_user += f"Расставьте артикли:\n"
    # res = await create_article_qwiz(selected_words)
    # print(res)
    await state.update_data(waiting_for_selected_exercises=exercises_translate_digits,
                            waiting_for_current_index=0,
                            waiting_for_correct_aswers=0)
    current_digit= exercises_translate_digits[0]
    digits_for_kb = random.sample(range(1, 1001), 2)
    translate_digit_list = [current_digit.digit] + digits_for_kb
    random.shuffle(translate_digit_list)

    TranslateDigitAction = create_enum_digit_from_data('TranslateDigitData', translate_digit_list)
    TranslateDigitData = create_callback_class_for_enum(TranslateDigitAction)

    try:
        await clbk.message.delete()  # 💥 удалить сообщение с кнопками
    except Exception as e:
        print(f"Не удалось удалить сообщение: {e}")
    await state.update_data(waiting_for_action_kb=TranslateDigitAction,
                            waiting_for_data_kb=TranslateDigitData,
                            )
    text_for_user += f"Как переводится это число:\n <b>{current_digit.correct_answer}</b>?"
    await clbk.message.answer(
        text=text_for_user,
        parse_mode=ParseMode.HTML,
        reply_markup=build_translate_digits_kb(TranslateDigitAction, TranslateDigitData)
    )
    #await send_article_quiz_poll(clbk.message, selected_words)

@router.callback_query(lambda c: c.data.startswith("translate_digits:") and not c.data.endswith(':cancel'))
async def handle_article_answer(clbk: CallbackQuery, state: FSMContext):
    print(clbk.data)
    await state.set_state(OrderExercisesTranslateDigits.waiting_for_selected_exercises)
    await state.set_state(OrderExercisesTranslateDigits.waiting_for_current_index)
    await state.set_state(OrderExercisesTranslateDigits.waiting_for_correct_answers)
    data = await state.get_data()
    exercises = data['waiting_for_selected_exercises']
    index = data['waiting_for_current_index']
    correct_count = data['waiting_for_correct_aswers']

    current_exercise = exercises[index]

    # допустим, в callback_data: "article:der"
    chosen_digit = int(clbk.data.split(":")[1])
    print(chosen_digit, current_exercise)
    if chosen_digit == current_exercise.digit:
        correct_count += 1
        await clbk.answer("✅ Правильно!")
    else:
        await clbk.answer(f"❌ Неверно. Правильный ответ: {current_exercise.digit}")

    index += 1

    if index < len(exercises):
        next_exercise = exercises[index]
        digits_for_kb = random.sample(range(1, 1001), 2)
        translate_digit_list = [next_exercise.digit] + digits_for_kb
        random.shuffle(translate_digit_list)
        TranslateDigitAction = create_enum_digit_from_data('TranslateDigitData', translate_digit_list)
        TranslateDigitData = create_callback_class_for_enum(TranslateDigitAction)
        text = f"Как переводится это число <b>{next_exercise.correct_answer}</b>?"
        await clbk.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=build_translate_digits_kb(TranslateDigitAction, TranslateDigitData))
    else:
        user = await get_user_async(BotDB.get_user_id(clbk.message.chat.id))
        await count_score_lifes(user, correct_count, len(exercises))
        text_for_user = f"Квиз завершён! Правильных ответов: {correct_count}/{len(exercises)}"
        text_for_user += f"{user.username}  Ваши баллы:{user.score},\n"
        text_for_user += f"  Ваши жизни: {user.lifes} \n\n"
        try:
            await clbk.message.delete()  # 💥 вместо clbk.message.delete()
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")
        await clbk.message.answer(
            text=text_for_user,
            parse_mode=ParseMode.HTML,
            reply_markup=build_exercises_kb()
        )

        #await clbk.message.edit_text(f"Квиз завершён! Правильных ответов: {correct_count}/{len(selected_words)}")
        await state.clear()  # можно очистить FSM

    # сохраняем новое состояние
    await state.update_data(
        waiting_for_current_index=index,
        waiting_for_correct_aswers=correct_count
    )




