import random

from enum import Enum
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class ExercisesDataAction(Enum):
    translate_words = 'translate_words'
    articles = 'articles'
    verb_forms = 'verb_forms'
    translate_digits = 'translate_digits'
    pronouns = 'proniouns'
    numeral = 'numeral'
    adjective = 'adjective'
    qwiz = 'qwiz'
    cancel = 'cancel'

class ExercisesData(CallbackData, prefix='exercises'):
    action: ExercisesDataAction
class ArticleDataAction(Enum):
    der = 'der'
    das = 'das'
    die = 'die'
    die_plural = 'die_plural'
    cancel = 'cancel'
class ArticleData(CallbackData, prefix='articles'):
    action: ArticleDataAction


class WordData(CallbackData, prefix="word"):
    idx: int
    selected: bool = False


def create_enum_from_data(enum_name, data):
    enum_members = {}
    for i, item in enumerate(data):
        enum_members[f"{i}_w"] = item.word
        enum_members[f"{i}_t"] = item.word_translate
    enum_members['cancel'] = 'cancel'
    return Enum(enum_name, enum_members)

def create_enum_digit_from_data(emun_name, data):
    print('create_enum', data)
    enum_members = {str(item): item for item in data}
    enum_members['cancel'] = 'cancel'
    print('enum_members', enum_members)
    return Enum(emun_name, enum_members)


def build_exercises_kb():
    print ('KWYBOARD_EXERCISES')

    translate_words = InlineKeyboardButton(
        text="📝Перевод слов",
        callback_data=ExercisesData(action=ExercisesDataAction.translate_words).pack()
    )
    articles = InlineKeyboardButton(
        text="📝Артикли",
        callback_data=ExercisesData(action=ExercisesDataAction.articles).pack()
    )
    verb_forms = InlineKeyboardButton(
        text="📝Формы глагола",
        callback_data=ExercisesData(action=ExercisesDataAction.verb_forms).pack()
    )
    translate_digits = InlineKeyboardButton(
        text="📝Перевод чисел",
        callback_data=ExercisesData(action=ExercisesDataAction.translate_digits).pack()
    )
    pronouns = InlineKeyboardButton(
        text="📝Местоимения",
        callback_data=ExercisesData(action=ExercisesDataAction.pronouns).pack()
    )
    numeral = InlineKeyboardButton(
        text="📝Числительные",
        callback_data=ExercisesData(action=ExercisesDataAction.numeral).pack()
    )
    adjectiv = InlineKeyboardButton(
        text="📝Прилагательные",
        callback_data=ExercisesData(action=ExercisesDataAction.adjective).pack()
    )
    qwiz = InlineKeyboardButton(
        text="📝Викторина",
        callback_data=ExercisesData(action=ExercisesDataAction.qwiz).pack()
    )

    cancel = InlineKeyboardButton(
        text='Отмена',
        callback_data=ExercisesData(action=ExercisesDataAction.cancel).pack()

    )

    first_line = [translate_words, articles, pronouns]
    second_line = [translate_digits, verb_forms, numeral]
    third_line = [adjectiv, qwiz, cancel]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[first_line, second_line, third_line],
    )
    return markup


def build_translate_words_kb(data, selected_dict, selected_left=None, selected_right=None, matched_pairs=None):
    builder = InlineKeyboardBuilder()
    if matched_pairs is None:
        matched_pairs = matched_pairs or []
    if selected_left is None:
        selected_left = selected_left or []
    if selected_right is None:
        selected_right = selected_right or []
    for key, value in selected_dict.items():
        print(key, value)
        if key != 'cancel':
            left_disabled = any(key[1].value in pair for pair in matched_pairs)
            left_text = f"✅ {key[1].value}" if key[1].value in selected_left else key[1].value
            button = builder.button(
                text=left_text,#key[1].value,
                callback_data=data(action=key[1]).pack(),
                disabled = left_disabled
            )
            right_disabled = any(value[1].value in pair for pair in matched_pairs)
            right_text = f"✅ {value[1].value}" if value[1].value in selected_right else value[1].value
            button = builder.button(
                text=right_text,#value[1].value,
                callback_data=data(action=value[1]).pack(),
                disabled=right_disabled
            )
        else:
            button = builder.button(
                text=value.value,
                callback_data=data(action=value).pack()
            )

    builder.adjust(2, 2, 2, 2, 2, 1)
    return builder.as_markup()


def build_article_quiz_kb():
    der = InlineKeyboardButton(
        text="der",
        callback_data=ArticleData(action=ArticleDataAction.der).pack()
    )
    das = InlineKeyboardButton(
        text="das",
        callback_data=ArticleData(action=ArticleDataAction.das).pack()
    )
    die = InlineKeyboardButton(
        text="die",
        callback_data=ArticleData(action=ArticleDataAction.die).pack()
    )
    die_plural = InlineKeyboardButton(
        text="die_plural",
        callback_data=ArticleData(action=ArticleDataAction.die_plural).pack()
    )
    cancel = InlineKeyboardButton(
        text="📝cancel",
        callback_data=ArticleData(action=ArticleDataAction.cancel).pack()
    )
    first_line = [der, das, die, die_plural]
    second_line = [cancel]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[first_line, second_line],
    )
    return markup

def build_translate_digits_kb(action, data):
    builder = InlineKeyboardBuilder()
    print(action._member_map_.items())
    for key, value in action._member_map_.items():
        print(key, value)
        if key != 'cancel':
            button = builder.button(
                text=str(value.value),
                callback_data=data(action=value).pack(),
            )
        else:
            button = builder.button(
                text=value.value,
                callback_data=data(action=value).pack()
            )

    builder.adjust(3)
    return builder.as_markup()
