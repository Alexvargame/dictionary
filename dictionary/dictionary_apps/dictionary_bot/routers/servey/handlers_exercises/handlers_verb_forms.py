from asgiref.sync import sync_to_async
import django
import os
import random
import asyncio

from aiogram import Router, F, types
#from aiogram.utils import markdown
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.filters.callback_data import CallbackData


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dictionary.config.django.base')
django.setup()


from dictionary.dictionary_apps.dictionary_bot.base_name import BotDB


from dictionary.dictionary_apps.dictionary_bot.keyboards.employee_kb.exercises_kb import (ExercisesData, ExercisesDataAction,
                                                                                          build_exercises_kb, build_article_quiz_kb,
                                                                                          VerbFormsDataAction, VerbFormsData,
                                                                                          build_verbs_form_kb, build_perfect_form_verb_kb,
                                                                                          create_enum_perfect_verb_from_data)
from dictionary.dictionary_apps.words.models import Noun
from dictionary.dictionary_apps.words.repository import VerbRepository, WordRepository
from dictionary.dictionary_apps.words.services import VerbService, WordService
from dictionary.dictionary_apps.words.selectors import  verb_get
from dictionary.dictionary_apps.users.selectors import user_get

from .data_file import separable_prefixes, inseparable_prefixes, umlauts_map
from ..states import OrderExercisesVerbForms, OrderExercisesVerbPresentForms, OrderExercisesVerbPrateritumForms
from .statistic import count_score_lifes


router = Router(name='verb_forms')
@sync_to_async
def create_verbs_ids():
    return VerbService(VerbRepository()).list_objects()

@sync_to_async
def create_words_ids(filters):
    return WordService(WordRepository()).list_objects(filters)

@sync_to_async
def get_verb_for_id(verb_id):
    return verb_get(verb_id)
@sync_to_async
def get_user_async(user_id):
    return user_get(user_id)
def create_callback_class_for_enum(enum_cls):
    class TranslateDigitsData(CallbackData, prefix='perfect_forms'):
        action: enum_cls
    return TranslateDigitsData
def change_vowel(verb):
    separable_prefixes = [
        "ab", "an", "auf", "aus", "bei", "ein", "fern",
        "mit", "nach", "vor", "weg", "zu", "zurück", "zusammen"
    ]

    # Inseparable prefixes — неотделяемые приставки
    inseparable_prefixes = [
        "be", "emp", "ent", "er", "ge", "miss", "ver", "zer",
    ]

    # Словарь обычная_буква -> буква_с_умлаутом
    umlauts_map = {
        "a": "ä",
        "o": "ö",
        "u": "ü",
        "A": "Ä",
        "O": "Ö",
        "U": "Ü",
        "ss": "ß"
    }

    verb_tem = verb
    for prefix in sorted(separable_prefixes, key=len, reverse=True):
        if verb.startswith(prefix):
            verb_tem = verb[len(prefix):]
            break
    for prefix in sorted(inseparable_prefixes, key=len, reverse=True):
        if verb.startswith(prefix):
            verb_tem = verb[len(prefix):]
            break
    for l in verb_tem:
        if l in [k for k in umlauts_map.keys()]:
            verb_tem = verb_tem.replace(l, umlauts_map[l])
        if l in [k for k in umlauts_map.values()]:
            kk = next((k for k, v in umlauts_map.items() if v == umlauts_map[kk]), None)
            verb_tem = verb_tem.replace(l, key)
    add_word = random.sample(['haben', 'sein'], k=1)
    verb_tem = add_word[0] + ' ' + verb_tem
    return verb_tem
    # Проверяем на неотделяемую приставку in inseparable_prefixes):
def add_ge_et_to_verb(verb):
    verb_tem = 'ge'+verb[:-2]+'et'
    add_word = random.sample(['haben', 'sein'], k=1)
    verb_tem = add_word[0] + ' ' + verb_tem
    return verb_tem

def add_et_to_verb(verb):
    verb_tem = verb[:-2]+'et'
    add_word = random.sample(['haben', 'sein'], k=1)
    verb_tem = add_word[0] + ' ' + verb_tem
    return verb_tem

random_verb_change_dict = {
    'vowel' :change_vowel,
    'ge_et' :add_ge_et_to_verb,
    'et': add_et_to_verb,
}


async def generate_present_verbs_form_for_exercises(verb):
    verbs_for_kb = []
    method_for = random.sample([k for k in random_verb_change_dict.keys()], 2)
    for m in method_for:
        verbs_for_kb.append(random_verb_change_dict[m](verb))
    return verbs_for_kb


@router.callback_query(ExercisesData.filter(F.action == ExercisesDataAction.verb_forms))
async def choice_verb_form(clbk:CallbackQuery, state:FSMContext):
    print(clbk.data)
    try:
        await clbk.message.delete()  # 💥 удалить сообщение с кнопками
    except Exception as e:
        print(f"Не удалось удалить сообщение: {e}")
    await clbk.message.answer(
        text = f"{clbk.data}",
        parse_mode=ParseMode.HTML,
        reply_markup=build_verbs_form_kb(),
    )

@router.callback_query(lambda c: c.data.startswith('verb_forms:') and not c.data.endswith(':cancel'))
async def create_exercises_articles(clbk: CallbackQuery, state: FSMContext):
    await state.set_state(OrderExercisesVerbForms.waiting_for_verb_form)
    await state.update_data(waiting_for_verb_form=clbk.data.split(':')[1])
    data = await state.get_data()
    if data['waiting_for_verb_form'] == 'perfect':
        await perfect_form(clbk, state)
    elif data['waiting_for_verb_form'] == 'present':
        await state.set_state(OrderExercisesVerbPresentForms.waiting_for_verb_form)
        await state.update_data(waiting_for_verb_form=clbk.data.split(':')[1])
        await present_form(clbk, state)
    elif data['waiting_for_verb_form'] == 'prateritum':
        pronouns = ['ich', 'du', 'er_sie_es', 'wir', 'ihr', 'Sie_sie']
        await state.set_state(OrderExercisesVerbPrateritumForms.waiting_for_verb_form)
        await state.update_data(waiting_for_verb_form=clbk.data.split(':')[1])
        await prateritum_form(clbk, state, pronouns)
    elif data['waiting_for_verb_form'] == 'prateritum_easy':
        pronouns = ['ich', 'Sie_sie', 'ich', 'Sie_sie', 'ich', 'Sie_sie']
        await state.set_state(OrderExercisesVerbPrateritumForms.waiting_for_verb_form)
        await state.update_data(waiting_for_verb_form=clbk.data.split(':')[1])
        await prateritum_form(clbk, state, pronouns)

async def perfect_form(clbk, state):
    print('EXERCISES_verbs_perfect', clbk.data)
    limit = 5
    filters = {}
    all_words = await create_verbs_ids()
    all_ids = [w.id for w in all_words]
    if len(all_ids) >= limit:
        random_ids = random.sample(all_ids, limit)
    filters = {'id__in': random_ids}
    selected_words = await create_words_ids(filters)
    print('sel', selected_words)
    await state.update_data(waiting_for_selected_verbs=selected_words)

    user = await get_user_async(BotDB.get_user_id(clbk.message.chat.id))
    text_for_user = f"{user.username}  Ваши баллы:{user.score},\n"
    text_for_user += f"  Ваши жизни: {user.lifes} \n\n"
    text_for_user += f"Выберите правильную форму глагола:\n"
    await state.update_data(waiting_for_selected_verbs=selected_words,
                            waiting_for_current_index=0,
                            waiting_for_correct_aswers=0)
    current_word = selected_words[0]
    added_verb_form = await generate_present_verbs_form_for_exercises(current_word.word)
    print(added_verb_form)
    added_verb_form = added_verb_form + [current_word.past_perfect_form]
    random.shuffle(added_verb_form)
    PerfectVerbFormAction = create_enum_perfect_verb_from_data('PerfectVerbFormData', added_verb_form)
    PerfectVerbFormData = create_callback_class_for_enum(PerfectVerbFormAction)
    text_for_user += f"Какая форма у глагола: <b>{current_word.word}</b>?"
    try:
        await clbk.message.delete()  # 💥 удалить сообщение с кнопками
    except Exception as e:
        print(f"Не удалось удалить сообщение: {e}")

    await clbk.message.answer(
        text=text_for_user,
        parse_mode=ParseMode.HTML,
        reply_markup=build_perfect_form_verb_kb(PerfectVerbFormAction, PerfectVerbFormData)
    )


@router.callback_query(lambda c: c.data.startswith("perfect_forms:") and not c.data.endswith(':cancel'))
async def handle_perfect_form_answer(clbk: CallbackQuery, state: FSMContext):
    await state.set_state(OrderExercisesVerbForms.waiting_for_selected_verbs)
    await state.set_state(OrderExercisesVerbForms.waiting_for_current_index)
    await state.set_state(OrderExercisesVerbForms.waiting_for_correct_answers)
    data = await state.get_data()
    selected_words = data['waiting_for_selected_verbs']
    index = data['waiting_for_current_index']
    correct_count = data['waiting_for_correct_aswers']
    current_word = selected_words[index]
    chosen_form = clbk.data.split(":")[1]
    if chosen_form == current_word.past_perfect_form:
        correct_count += 1
        await clbk.answer("✅ Правильно!")
    else:
        await clbk.answer(f"❌ Неверно. Правильный ответ: {current_word.past_perfect_form}")

    index += 1

    if index < len(selected_words):
        next_word = selected_words[index]
        added_verb_form = await generate_present_verbs_form_for_exercises(next_word.word)
        added_verb_form = added_verb_form + [next_word.past_perfect_form]
        random.shuffle(added_verb_form)
        PerfectVerbFormAction = create_enum_perfect_verb_from_data('PerfectVerbFormData', added_verb_form)
        PerfectVerbFormData = create_callback_class_for_enum(PerfectVerbFormAction)
        text = f"Какая форма у глагола: <b>{next_word.word}</b>?"
        await clbk.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=build_perfect_form_verb_kb(PerfectVerbFormAction, PerfectVerbFormData)
        )
    else:
        user = await get_user_async(BotDB.get_user_id(clbk.message.chat.id))
        await count_score_lifes(user, correct_count, len(selected_words))
        text_for_user = f"Квиз завершён! Правильных ответов: {correct_count}/{len(selected_words)}\n"
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

        await state.clear()  # можно очистить FSM

    # сохраняем новое состояние
    await state.update_data(
        waiting_for_current_index=index,
        waiting_for_correct_aswers=correct_count
    )


async def present_form(clbk, state):
    pronouns = ['ich', 'du', 'er_sie_es', 'wir', 'ihr', 'Sie_sie']
    print('EXERCISES_verbs_present', clbk.data)
    limit = 5
    filters = {}
    all_words = await create_verbs_ids()
    all_ids = [w.id for w in all_words]
    if len(all_ids) >= limit:
        random_ids = random.sample(all_ids, limit)
    filters = {'id__in': random_ids}
    selected_words = await create_words_ids(filters)
    selected_pronouns = random.sample(pronouns, limit)
    user = await get_user_async(BotDB.get_user_id(clbk.message.chat.id))
    text_for_user = f"{user.username}  Ваши баллы:{user.score},\n"
    text_for_user += f"  Ваши жизни: {user.lifes} \n\n"
    text_for_user += f"Выберите правильную форму глагола для местоимения:\n"
    await state.update_data(waiting_for_selected_verbs=selected_words,
                            waiting_for_selected_pronouns=selected_pronouns,
                            waiting_for_current_index=0,
                            waiting_for_correct_aswers=0)
    current_word = selected_words[0]
    current_pronoun = selected_pronouns[0]
    text_for_user += f"Какая форма у глагола: <b>{current_word.word}</b> \n для местоимения {current_pronoun}?"
    try:
        await clbk.message.delete()  # 💥 удалить сообщение с кнопками
    except Exception as e:
        print(f"Не удалось удалить сообщение: {e}")

    await clbk.message.answer(
        text=text_for_user,
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(OrderExercisesVerbPresentForms.waiting_for_verb_form_for_pronoun)


@router.message(StateFilter(OrderExercisesVerbPresentForms.waiting_for_verb_form_for_pronoun))
async def handle_present_form_answer(msg:types.Message, state: FSMContext):
    print("CURRENT STATE IN CALLBACK:", await state.get_state())
    data = await state.get_data()
    selected_verbs = data['waiting_for_selected_verbs']
    selected_pronouns = data['waiting_for_selected_pronouns']
    index = data['waiting_for_current_index']
    correct_count = data['waiting_for_correct_aswers']
    current_word = selected_verbs[index]
    chosen_form = msg.text.lower()
    print('CHOSEN_FORM', chosen_form)
    field_name = f"{selected_pronouns[index]}_form"
    correct_answer = getattr(selected_verbs[index], field_name)


    if chosen_form == correct_answer:
        correct_count += 1
        await msg.answer("✅ Правильно!")
    else:
        await msg.answer(f"❌ Неверно. Правильный ответ: {correct_answer}")

    index += 1

    if index < len(selected_verbs):
        next_word = selected_verbs[index]
        next_pronoun = selected_pronouns[index]
        text =   f"Какая форма у глагола: <b>{next_word.word}</b> \n для местоимения {next_pronoun}?"
        await msg.answer(
            text,
            parse_mode="HTML",
            #reply_markup=build_present_form_verb_kb(PresentVerbFormAction, PresentVerbFormData)
        )
        await state.set_state(OrderExercisesVerbPresentForms.waiting_for_verb_form_for_pronoun)
    else:

        user = await get_user_async(BotDB.get_user_id(msg.chat.id))
        await count_score_lifes(user, correct_count, len(selected_verbs))
        text_for_user = f"Квиз завершён! Правильных ответов: {correct_count}/{len(selected_verbs)}\n"
        text_for_user += f"{user.username}  Ваши баллы:{user.score},\n"
        text_for_user += f"  Ваши жизни: {user.lifes} \n\n"
        try:
            await msg.delete()  # 💥 вместо clbk.message.delete()
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")
        await msg.answer(
            text=text_for_user,
            parse_mode=ParseMode.HTML,
            reply_markup=build_exercises_kb()
        )

        await state.clear()  # можно очистить FSM

    # сохраняем новое состояние
    await state.update_data(
        waiting_for_current_index=index,
        waiting_for_correct_aswers=correct_count
    )

async def prateritum_form(clbk, state, pronouns):
    #pronouns = ['ich', 'du', 'er_sie_es', 'wir', 'ihr', 'Sie_sie']
    print('EXERCISES_verbs_prateritum', clbk.data)
    limit = 5
    filters = {}
    all_words = await create_verbs_ids()
    all_ids = [w.id for w in all_words]
    if len(all_ids) >= limit:
        random_ids = random.sample(all_ids, limit)
    filters = {'id__in': random_ids}
    selected_verbs = await create_words_ids(filters)
    selected_pronouns = random.sample(pronouns, limit)
    user = await get_user_async(BotDB.get_user_id(clbk.message.chat.id))
    text_for_user = f"{user.username}  Ваши баллы:{user.score},\n"
    text_for_user += f"  Ваши жизни: {user.lifes} \n\n"
    text_for_user += f"Выберите правильную форму глагола для местоимения:\n"
    await state.update_data(waiting_for_selected_verbs=selected_verbs,
                            waiting_for_selected_pronouns=selected_pronouns,
                            waiting_for_current_index=0,
                            waiting_for_correct_aswers=0)
    current_verb = selected_verbs[0]
    current_pronoun = selected_pronouns[0]
    text_for_user += f"Какая форма у глагола: <b>{current_verb.word}</b> \n для местоимения {current_pronoun}?"
    try:
        await clbk.message.delete()  # 💥 удалить сообщение с кнопками
    except Exception as e:
        print(f"Не удалось удалить сообщение: {e}")

    await clbk.message.answer(
        text=text_for_user,
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(OrderExercisesVerbPrateritumForms.waiting_for_verb_form_for_pronoun)

@router.message(StateFilter(OrderExercisesVerbPrateritumForms.waiting_for_verb_form_for_pronoun))
async def handle_prateritum_form_answer(msg:types.Message, state: FSMContext):

    print("CURRENT STATE IN CALLBACK:", await state.get_state())
    data = await state.get_data()
    selected_verbs = data['waiting_for_selected_verbs']
    selected_pronouns = data['waiting_for_selected_pronouns']
    index = data['waiting_for_current_index']
    correct_count = data['waiting_for_correct_aswers']
    current_verb = selected_verbs[index]
    chosen_form = msg.text.lower()
    print('CHOSEN_FORM_Prat', chosen_form)
    field_name = f"past_prateritum_{selected_pronouns[index]}_form"
    correct_answer = getattr(selected_verbs[index], field_name)


    if chosen_form == correct_answer:
        correct_count += 1
        await msg.answer("✅ Правильно!")
    else:
        await msg.answer(f"❌ Неверно. Правильный ответ: {correct_answer}")

    index += 1

    if index < len(selected_verbs):
        next_verb = selected_verbs[index]
        next_pronoun = selected_pronouns[index]
        text =   f"Какая форма у глагола: <b>{next_verb.word}</b> \n для местоимения {next_pronoun}?"
        await msg.answer(
            text,
            parse_mode="HTML",
            #reply_markup=build_present_form_verb_kb(PresentVerbFormAction, PresentVerbFormData)
        )
        await state.set_state(OrderExercisesVerbPrateritumForms.waiting_for_verb_form_for_pronoun)
    else:

        user = await get_user_async(BotDB.get_user_id(msg.chat.id))
        await count_score_lifes(user, correct_count, len(selected_verbs))
        text_for_user = f"Квиз завершён! Правильных ответов: {correct_count}/{len(selected_verbs)}\n"
        text_for_user += f"{user.username}  Ваши баллы:{user.score},\n"
        text_for_user += f"  Ваши жизни: {user.lifes} \n\n"
        try:
            await msg.delete()  # 💥 вместо clbk.message.delete()
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")
        await msg.answer(
            text=text_for_user,
            parse_mode=ParseMode.HTML,
            reply_markup=build_exercises_kb()
        )

        await state.clear()  # можно очистить FSM

    # сохраняем новое состояние
    await state.update_data(
        waiting_for_current_index=index,
        waiting_for_correct_aswers=correct_count
    )
