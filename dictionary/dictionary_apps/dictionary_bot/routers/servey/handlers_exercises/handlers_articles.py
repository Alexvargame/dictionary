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
                                                                                          build_exercises_kb, build_article_quiz_kb)
from dictionary.dictionary_apps.words.models import Noun
from dictionary.dictionary_apps.words.repository import NounRepository, WordRepository
from dictionary.dictionary_apps.words.services import NounService, WordService
from dictionary.dictionary_apps.words.selectors import  noun_get
from dictionary.dictionary_apps.users.selectors import user_get

from ..states import OrderExercisesArticle
from .statistic import count_score_lifes


router = Router(name='articles')
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


# async def send_article_quiz_poll(message, words):
#     for word in words:
#         question = f"Какой артикль у слова {word.word}?"
#         options = ['der', 'die', 'das', 'die.']
#         correct_option_id = options.index(word.article.name)  # индекс правильного ответа
#
#         await message.answer_poll(
#             question=question,
#             options=options,
#             type='quiz',            # важно: 'quiz', чтобы был правильный ответ
#             correct_option_id=correct_option_id,
#             is_anonymous=False
#         )

# async def create_article_qwiz(words):
#     qwiz_str_list = []
#     qwiz_word = None
#     for word in words:
#         answer_words = ['der', 'die', 'das', 'die.']
#         question_word = word.word
#         richt_answer = answer_words.index(word.article.name)
#         qwiz_str = (f"Какой артикль у слова {question_word}? | {answer_words[0]} | "
#                     f"{answer_words[1]} | {answer_words[2]} | {richt_answer}")
#         qwiz_str_list.append(qwiz_str)
#     return qwiz_str_list

@router.callback_query(ExercisesData.filter(F.action == ExercisesDataAction.articles))
async def create_exercises_articles(clbk: CallbackQuery, state: FSMContext):
    print('EXERCISES_ARTICLES ')
    limit = 5
    filters = {}
    all_words = await create_nouns_ids()
    all_ids = [w.id for w in all_words]
    if len(all_ids) >= limit:
        random_ids = random.sample(all_ids, limit)
    filters = {'id__in': random_ids}
    selected_words = await create_words_ids(filters)
    print('sel', selected_words)
    await state.update_data(waiting_for_selected_words=selected_words)
    user = await get_user_async(BotDB.get_user_id(clbk.message.chat.id))
    text_for_user = f"{user.username}  Ваши баллы:{user.score},\n"
    text_for_user += f"  Ваши жизни: {user.lifes} \n\n"
    text_for_user += f"Расставьте артикли:\n"
    # res = await create_article_qwiz(selected_words)
    # print(res)
    await state.update_data(waiting_for_selected=selected_words,
                            waiting_for_current_index=0,
                            waiting_for_correct_aswers=0)
    current_word = selected_words[0]
    text_for_user += f"Какой артикль у слова <b>{current_word.word}</b>?"
    try:
        await clbk.message.delete()  # 💥 удалить сообщение с кнопками
    except Exception as e:
        print(f"Не удалось удалить сообщение: {e}")

    await clbk.message.answer(
        text=text_for_user,
        parse_mode=ParseMode.HTML,
        reply_markup=build_article_quiz_kb()
    )
    #await send_article_quiz_poll(clbk.message, selected_words)

@router.callback_query(lambda c: c.data.startswith("articles:") and not c.data.endswith(':cancel'))
async def handle_article_answer(clbk: CallbackQuery, state: FSMContext):
    await state.set_state(OrderExercisesArticle.waiting_for_selected_words)
    await state.set_state(OrderExercisesArticle.waiting_for_current_index)
    await state.set_state(OrderExercisesArticle.waiting_for_correct_answers)
    data = await state.get_data()
    selected_words = data['waiting_for_selected']
    index = data['waiting_for_current_index']
    correct_count = data['waiting_for_correct_aswers']

    current_word = selected_words[index]

    # допустим, в callback_data: "article:der"
    chosen_article = clbk.data.split(":")[1]
    if chosen_article == 'die_plural':
        chosen_article = 'die.'
    if chosen_article == current_word.article.name:
        correct_count += 1
        await clbk.answer("✅ Правильно!")
    else:
        await clbk.answer(f"❌ Неверно. Правильный ответ: {current_word.article.name}")

    index += 1

    if index < len(selected_words):
        next_word = selected_words[index]
        text = f"Какой артикль у слова <b>{next_word.word}</b>?"
        await clbk.message.edit_text(text, parse_mode="HTML", reply_markup=build_article_quiz_kb())
    else:
        user = await get_user_async(BotDB.get_user_id(clbk.message.chat.id))
        await count_score_lifes(user, correct_count, len(selected_words))
        text_for_user = f"Квиз завершён! Правильных ответов: {correct_count}/{len(selected_words)}"
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




