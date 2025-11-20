from asgiref.sync import sync_to_async
import django
import os
import random

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram.filters.callback_data import CallbackData


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dictionary.config.django.base')
django.setup()


from dictionary.dictionary_apps.dictionary_bot.base_name import BotDB


from dictionary.dictionary_apps.dictionary_bot.keyboards.employee_kb.exercises_kb import (ExercisesData, ExercisesDataAction,
                                                                                          build_exercises_kb, build_form_pronoun_kb,
                                                                                          create_enum_pronouns_from_data)
#from dictionary.dictionary_apps.words.models import Pronoun
from dictionary.dictionary_apps.words.repository import PronounRepository, WordRepository
from dictionary.dictionary_apps.words.services import PronounService, WordService
from dictionary.dictionary_apps.words.selectors import   pronoun_list
from dictionary.dictionary_apps.users.selectors import user_get

from ..states import OrderExercisesPronouns
from .statistic import count_score_lifes


router = Router(name='pronouns')

PRONOUN_QWIZ_LIMIT = 5
@sync_to_async
def create_pronouns_ids():
    return PronounService(PronounRepository()).list_objects()

@sync_to_async
def create_words_ids(filters):
    return WordService(WordRepository()).list_objects(filters)
@sync_to_async
def get_pronoun_for_id(pronoun_id):
    return pronoun_get(pronoun_id)
@sync_to_async
def get_user_async(user_id):
    return user_get(user_id)

@sync_to_async
def get_pronouns_list():
    return pronoun_list()
@sync_to_async
def get_added_values(casuses):
    added_values = []
    for pronuns in pronoun_list():
        for casus in casuses:
            added_values.append(getattr(pronuns, casus))
    print(added_values)
    return added_values


def create_callback_class_for_enum(enum_cls):
    class TranslateDigitsData(CallbackData, prefix='pronouns'):
        action: enum_cls
    return TranslateDigitsData

async def get_user_stats_text(chat_id):
    user = await get_user_async(BotDB.get_user_id(chat_id))
    return f"{user.username}  Ваши баллы:{user.score},\nВаши жизни: {user.lifes}\n\n"


async def select_random_pronouns(limit):
    filters = {}
    all_pronouns = await create_pronouns_ids()
    all_ids = [w.id for w in all_pronouns]
    if len(all_ids) >= limit:
        random_ids = random.sample(all_ids, limit)
    filters = {'id__in': random_ids}
    return await create_words_ids(filters)
@router.callback_query(ExercisesData.filter(F.action == ExercisesDataAction.pronouns))
async def create_exercises_pronouns(clbk: CallbackQuery, state: FSMContext):
    print('EXERCISES_PRONOUNS')
    casuses = ['akkusativ', 'dativ', 'prossessive', 'reflexive',]
    selected_pronouns = await select_random_pronouns(PRONOUN_QWIZ_LIMIT)
    selected_casuses = random.choices(casuses, k=PRONOUN_QWIZ_LIMIT)
    all_values = await get_added_values(casuses)
    await state.update_data(waiting_for_selected_pronouns=selected_pronouns)
    await state.update_data(waiting_for_selected_casuses=selected_casuses)
    await state.update_data(waiting_for_all_values=all_values)
    text_for_user = await get_user_stats_text(clbk.message.chat.id)
    text_for_user += f"Выберите форму местоимения:\n"
    await state.update_data(waiting_for_selected_pronouns=selected_pronouns,
                            waiting_for_current_index=0,
                            waiting_for_correct_aswers=0)
    current_pronoun = selected_pronouns[0]
    current_casus = selected_casuses[0]
    added_values = random.sample(all_values, 2)
    correct_answer = getattr(current_pronoun, current_casus)
    added_values.append(correct_answer)
    random.shuffle(added_values)
    PronounFormAction = create_enum_pronouns_from_data('PronounFormData', added_values)
    PronounFormData = create_callback_class_for_enum(PronounFormAction)
    text_for_user += f"Какая форма у местоимения <b>{current_pronoun.word}</b> в этом падеже  <b>{current_casus}</b>?"
    try:
        await clbk.message.delete()  # 💥 удалить сообщение с кнопками
    except Exception as e:
        print(f"Не удалось удалить сообщение: {e}")

    await clbk.message.answer(
        text=text_for_user,
        parse_mode=ParseMode.HTML,
        reply_markup=build_form_pronoun_kb(PronounFormAction, PronounFormData)
    )

@router.callback_query(lambda c: c.data.startswith("pronouns:") and not c.data.endswith(':cancel'))
async def handle_article_answer(clbk: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_pronuons = data['waiting_for_selected_pronouns']
    index = data['waiting_for_current_index']
    correct_count = data['waiting_for_correct_aswers']
    selected_casuses = data['waiting_for_selected_casuses']
    all_values = data['waiting_for_all_values']

    current_pronoun = selected_pronuons[index]
    current_casus = selected_casuses[index]
    added_values = random.sample(all_values, 2)
    correct_answer = getattr(current_pronoun, current_casus)
    added_values.append(correct_answer)
    random.shuffle(added_values)
    chosen_form = clbk.data.split(":")[1]
    if chosen_form == getattr(current_pronoun, current_casus):
        correct_count += 1
        await clbk.answer("✅ Правильно!")
    else:
        await clbk.answer(f"❌ Неверно. Правильный ответ: {correct_answer}")

    index += 1

    if index < len(selected_pronuons):
        next_pronoun = selected_pronuons[index]
        next_casus = selected_casuses[index]
        PronounFormAction = create_enum_pronouns_from_data('PronounFormData', added_values)
        PronounFormData = create_callback_class_for_enum(PronounFormAction)
        text = f"Какая форма у местоимения <b>{current_pronoun.word}</b> в этом падеже  <b>{current_casus}</b>?"

        await clbk.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=build_form_pronoun_kb(PronounFormAction, PronounFormData)
        )
    else:
        user = await get_user_async(BotDB.get_user_id(clbk.message.chat.id))
        await count_score_lifes(user, correct_count, len(selected_pronuons))
        text_for_user = f"Квиз завершён! Правильных ответов: {correct_count}/{len(selected_pronuons)}"
        text_for_user += await get_user_stats_text(clbk.message.chat.id)
        try:
            await clbk.message.delete()
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")
        await clbk.message.answer(
            text=text_for_user,
            parse_mode=ParseMode.HTML,
            reply_markup=build_exercises_kb()
        )
        await state.clear()  # можно очистить FSM
    await state.update_data(
        waiting_for_current_index=index,
        waiting_for_correct_aswers=correct_count
    )




