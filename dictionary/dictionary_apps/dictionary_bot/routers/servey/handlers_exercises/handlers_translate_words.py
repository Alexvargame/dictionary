from asgiref.sync import sync_to_async
import django
import os
import random

from aiogram import Router, F, types
from aiogram.utils import markdown
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram.filters.callback_data import CallbackData


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dictionary.config.django.base')
django.setup()
#from estate_agency.estate_bot.db import BotDBClass


from dictionary.dictionary_apps.dictionary_bot.base_name import BotDB

from dictionary.dictionary_apps.dictionary_bot.keyboards.employee_kb.main_employee_kb import (build_cancel_kb, build_next_cancel_kb,
                                                                                              NextCancelData, NextCancelDataAction,
                                                                                              CancelData, CancelDataAction,
                                                                                              build_admin_kb, build_employee_kb)
from dictionary.dictionary_apps.dictionary_bot.keyboards.employee_kb.exercises_kb import (ExercisesData, ExercisesDataAction,
                                                                                          build_exercises_kb, build_translate_words_kb,
                                                                                          # TranslateWord, TranslateWordAction,
                                                                                          create_enum_from_data)
from dictionary.dictionary_apps.words.models import Word
from dictionary.dictionary_apps.words.repository import WordRepository
from dictionary.dictionary_apps.words.services import WordService
from dictionary.dictionary_apps.words.selectors import  word_get
from dictionary.dictionary_apps.users.selectors import user_get
# from dictionary.dictionary_apps.users.models import BaseUser
from dictionary.dictionary_apps.dtos.words.response_dto import (NounPaarExerciseGermanDTO, VerbPaarExerciseGermanDTO,
                                                                RussianPaarExerciseGermanDTO, WordPaarTranslateExerciseDTO)
from ..states import OrderExercises
from .statistic import count_score_lifes
from dictionary.dictionary_apps.dictionary_bot.keyboards.employee_kb.dictionarys_for_kb import kb_dict_cancel
router = Router(name='translate_words')
@sync_to_async
def create_words_ids(filters):
    return WordService(WordRepository()).list_objects(filters)

@sync_to_async
def get_word_for_id(word_id):
    return word_get(word_id)
@sync_to_async
def get_user_async(user_id):
    return user_get(user_id)

def shuffle_dict(dictionary):
    new_dict = dict.fromkeys([(k,v) for (k, v) in dictionary if 'w' in k])

    tmp_values = [(k,v) for (k, v) in dictionary if 't' in k]

    random.shuffle(tmp_values)
    for key in new_dict.keys():

        if key[0] != 'cancel':
            new_dict[key] = tmp_values[0]
            tmp_values.pop(0)

    new_dict['cancel'] = [v for (k,v) in dictionary if k=='cancel'][0]
    print(new_dict)
   # ('cancel', < TranslateWordsData.cancel: 'Отмена' >)
    return new_dict

async def create_exercises_translate_words(clbk: CallbackQuery, state: FSMContext):
    global TranslateWordAction
    global TranslateWord
    limit = 15
    german_list = []
    russian_list = []
    translate_word_list = []
    filters = {}
    all_words = await create_words_ids(filters)
    all_ids = [w.id for w in all_words]
    if len(all_ids) >= limit:
        random_ids = random.sample(all_ids, limit)
    filters = {'id__in': random_ids}

    selected_words = []
    tmp_selected = await create_words_ids(filters)
    while limit > 5 and len(selected_words) < 5:
        if len(tmp_selected[limit - 1].word_translate.encode('utf-8')) <= 64:
            selected_words.append(tmp_selected[limit - 1])
        limit -= 1
    print('sel', selected_words)
    await state.update_data(waiting_for_selected_words=selected_words)
    for word in selected_words:
        if word.word_type.name == 'Noun':
            translate_word_list.append(
                WordPaarTranslateExerciseDTO(
                    **{'id': word.id, 'article': word.article.name,
                       'word': word.word, 'word_type': word.word_type.name,
                       'word_translate': word.word_translate}
                )
            )
        else:
            translate_word_list.append(
                WordPaarTranslateExerciseDTO(
                    **{'id': word.id, 'article': '',
                       'word': word.word, 'word_type': word.word_type.name,
                       'word_translate': word.word_translate}
                )
            )

    for word in selected_words:
        if word.word_type.name == 'Noun':
            german_list.append(
                NounPaarExerciseGermanDTO(
                    **{'id': word.id, 'article': word.article.name,
                       'word': word.word, 'word_type': word.word_type.name}
                )
            )
            russian_list.append(
                RussianPaarExerciseGermanDTO(
                    **{
                        'id': word.id,
                        'word_translate': word.word_translate
                    }
                )
            )

        else: #elif word.word_type.name == 'Verb':
            german_list.append(
                VerbPaarExerciseGermanDTO(
                    **{'id': word.id, 'article': '',
                       'word': word.word, 'word_type': word.word_type.name}
                )
            )
            russian_list.append(
                RussianPaarExerciseGermanDTO(
                    **{
                        'id': word.id,
                        'word_translate': word.word_translate
                    }
                )
            )
    random.shuffle(german_list)
    random.shuffle(russian_list)
    await state.update_data(waiting_for_selected_words=german_list+russian_list)
    user = await get_user_async(BotDB.get_user_id(clbk.message.chat.id))
    text_for_user = f"{user.username}  Ваши баллы:{user.score},\n"
    text_for_user += f"  Ваши жизни: {user.lifes} \n\n"
    text_for_user += f"Переведите слова:\n"
    # text_for_user += "🇩🇪 Немецкие:\n"
    # for ger in german_list:
    #     if ger.word_type == 'Noun':
    #         text_for_user += ger.article +' '+ ger.word + "\n"
    #     else:
    #         text_for_user += ger.word + "\n"
    # text_for_user += "\n"
    # text_for_user += "🇷🇺 Русские:\n"
    # for rus in russian_list:
    #     text_for_user += rus.word_translate + "\n"
    # text_for_user += "\n\nНапиши ответ в виде: <code>1A, 2B...</code>"
    try:
        await clbk.message.delete()  # 💥 удалить сообщение с кнопками
    except Exception as e:
        print(f"Не удалось удалить сообщение: {e}")
    TranslateWordAction = create_enum_from_data('TranslateWordsData', translate_word_list)
    class TranslateWord(CallbackData, prefix='translate_words'):
        action: TranslateWordAction
    await state.update_data(waiting_for_action=TranslateWordAction)

    selected_dict = shuffle_dict(TranslateWordAction._member_map_.items())

    await clbk.message.answer(
        text=text_for_user,
        parse_mode=ParseMode.HTML,
        reply_markup=build_translate_words_kb(TranslateWord, selected_dict,
                                              selected_left=None, selected_right=None,
                                              matched_pairs=None),
    )
    await state.set_state(OrderExercises.waiting_for_pair_words)
    await state.update_data(waiting_for_list_words=selected_dict)
    await state.update_data(
        selected_left=[],
        selected_right=[],
        matched_pairs=[],
        waiting_for_tmp_right=None,
        waiting_for_tmp_left=None,
    )




@router.callback_query(ExercisesData.filter(F.action == ExercisesDataAction.translate_words))
async def get_exesrcise_translate_words(clbk: CallbackQuery, state: FSMContext):
    await create_exercises_translate_words(clbk, state)

@router.callback_query(NextCancelData.filter(F.action == NextCancelDataAction.continue_exercises))
async def continue_exesrcise_translate_words(clbk: CallbackQuery, state: FSMContext):
    await create_exercises_translate_words(clbk, state)


@router.callback_query(lambda c: 'cancel' in c.data)
async def cancel_button(clbk: CallbackQuery):
    print(clbk.data)
    admin_employee = ''
    user_id = BotDB.get_user_id(clbk.message.chat.id)
    user = await get_user_async(user_id)
    if user.is_admin:
        admin_employee = 'A'
    else:
        admin_employee = 'E'

    try:
        await clbk.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение: {e}")
    print(kb_dict_cancel[clbk.data])
    await clbk.message.answer(
        text="Выберите упражнение:",
        parse_mode=ParseMode.HTML,
        reply_markup=kb_dict_cancel[clbk.data][admin_employee](),
    )


@router.callback_query(lambda c: c.data.startswith('translate_words:') and not c.data.endswith(':cancel'))
async def handle_dynamic_translate_buttons(clbk: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_left = data.get("selected_left", [])
    selected_right = data.get("selected_right", [])
    matched_pairs = data.get("matched_pairs", [])
    print('Lrft', selected_left, 'richr', selected_right,'pai', matched_pairs)
    # print('DATA_BUTTON actio', data)
    action_str = clbk.data.split(":", 1)[1]
    # print("Callback data:", clbk.data)
    # print("Action =", action_str)
    action_enum = TranslateWordAction(action_str)  # action_str из clbk.data
    action_value = action_enum.value
    # print('action_enum', action_enum, action_enum.name)
    # print('action_value', action_value)
    #
    # # Получаем текущее состояние
    #
    # # Определяем колонку
    # print(action_enum.name.endswith('_w'))
    # print(action_enum.name.endswith('_t'))
    if action_enum.name.endswith('_w'):  # левая колонка
        if action_value in selected_left:
            selected_left.remove(action_value)
        else:
            selected_left.append(action_value)
            await state.update_data(waiting_for_tmp_left=action_value)
            data = await state.get_data()
    elif action_enum.name.endswith('_t'):  # правая колонка
        if action_value in selected_right:
            selected_right.remove(action_value)
        else:
            selected_right.append(action_value)
            await state.update_data(waiting_for_tmp_right = action_value)
            data = await state.get_data()
    # Если обе кнопки выбраны — формируем пару
    print('TEMPWAIT',data['waiting_for_tmp_left'], data['waiting_for_tmp_right'])
    if data['waiting_for_tmp_left'] and data['waiting_for_tmp_right']:
        # Добавляем пару в список
        matched_pairs.append((data['waiting_for_tmp_left'], data['waiting_for_tmp_right']))
        # Сбрасываем текущие выборы
        await state.update_data(waiting_for_tmp_left= None)
        await state.update_data(waiting_for_tmp_right= None)
        print('PAIRS', matched_pairs)

        # 🔹 Здесь можно пересоздать клавиатуру через build_translate_words_kb
        # с параметром matched_pairs, чтобы закрасить выбранные и заблокировать их
        # например: reply_markup=build_translate_words_kb(TranslateWordAction, TranslateWord, matched_pairs=matched_pairs)

        # Сохраняем обратно в FSM
    await state.update_data(
        selected_left=selected_left,
        selected_right=selected_right,
        matched_pairs=matched_pairs
    )
    kb_translate_words = build_translate_words_kb(
        TranslateWord,
        selected_dict=data['waiting_for_list_words'],
        selected_left=selected_left,
        selected_right=selected_right,
        matched_pairs=matched_pairs,
    )
    await clbk.message.edit_reply_markup(
        reply_markup=kb_translate_words,
    )
    print('CCHEK_LEN', len(matched_pairs) , (len(sum(kb_translate_words.inline_keyboard, [])) - 1) / 2)
    if len(matched_pairs) >= (len(sum(kb_translate_words.inline_keyboard, [])) -1) / 2 :
        # 5 пар уже составлены — завершение упражнения
        # можно отправить результат пользователю
        await state.update_data(waiting_for_pair_words=matched_pairs)
        await clbk.message.answer("Все пары составлены!\n")
        text_pairs =  f"Сформированные пары:\n "
        for pair in matched_pairs:
            text_pairs += f"{pair[0]} -> {pair[1]}\n"
        await clbk.message.answer(text_pairs)
        # Для отладки пока просто показываем пользователю текущие пары
        #await state.set_state(OrderExercises.waiting_for_answer)
        await check_ordering_answer(clbk.message, state)


@router.message(OrderExercises.waiting_for_answer)
async def check_ordering_answer(msg: types.Message, state: FSMContext):
    try:
        await msg.delete()  # 💥 вместо clbk.message.delete()
    except Exception as e:
        print(f"Не удалось удалить сообщение: {e}")
    print('CHECk_ANSWER')
    user_answer = msg.text.strip()
    data = await state.get_data()
    print(data)
    selected = data.get("waiting_for_selected_words", [])
    print(selected)
    # Здесь можно сделать проверку — сравнить пары
    # Пока просто вернём правильные соответствия
    pairs = data.get('waiting_for_pair_words')
    print('PAIRS', pairs)
    tmp_ids = []
    correct_pairs = []
    correct_pairs_text = ''
    for sel in selected:
        if sel.id not in tmp_ids:
            w = await get_word_for_id(sel.id)
            correct_pairs_text += f"{w.word} → {w.word_translate}\n"
            tmp_ids.append(sel.id)
            correct_pairs.append((w.word, w.word_translate))
    print(correct_pairs)
    print(correct_pairs_text)
    try:
        await clbk.message.delete()  # 💥 удалить сообщение с кнопками
    except Exception as e:
        print(f"Не удалось удалить сообщение: {e}")
    # Сравниваем результаты:
    correct_answers = 0
    for pair in correct_pairs:
        if pair in pairs:
            correct_answers +=1
    user = await get_user_async(BotDB.get_user_id(msg.chat.id))
    await count_score_lifes(user, correct_answers, len(pairs))
    result_text = f"✅ Правильные пары:\n{correct_pairs_text}"
    result_text += f"\n {correct_answers} правильных ответов из {len(pairs)}\n"
    result_text += f"{user.username}  Ваши баллы:{user.score},\n"
    result_text += f"  Ваши жизни: {user.lifes} \n\n"
    await msg.answer(
        text = result_text,
        parse_mode=ParseMode.HTML,
        reply_markup=build_next_cancel_kb()
    )
    await state.clear()