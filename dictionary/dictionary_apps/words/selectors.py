from typing import Optional

from django.db.models.query import QuerySet

from dictionary.dictionary_apps.common.utils import (get_object)
from dictionary.dictionary_apps.words.filters import WordFilter, NounFilter, VerbFilter
from dictionary.dictionary_apps.words.models import Word, Lection, Article, Book, Noun, WordType, Verb


def word_list(*, filters=None):
    filters = filters or {}
    qs = Word.objects.select_subclasses().filter(**filters)
    return WordFilter(filters, qs).qs

def word_get(word_id):
    word = get_object(Word, id=word_id)
    return word

def noun_list(*, filters=None):
    filters = filters or {}
    qs = Noun.objects.all()
    return NounFilter(filters, qs).qs

def verb_get(verb_id):
    verb = get_object(Verb, id=verb_id)
    return  verb

def verb_list(*, filters=None):
    filters = filters or {}
    qs = Verb.objects.all()
    return VerbFilter(filters, qs).qs

def noun_get(noun_id):
    noun = get_object(Noun, id=noun_id)
    return noun
def lection_get(lection_id):
    lection = get_object(Lection, id=lection_id)
    return lection

def word_type_get(word_type_id):
    word_type = get_object(WordType, id=word_type_id)
    return word_type

def book_get(book_id):
    book = get_object(Book, id=book_id)
    return book

def article_get(article_id):
    article = get_object(Article, id=article_id)
    return article

























































