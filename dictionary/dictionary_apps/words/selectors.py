from typing import Optional

from django.db.models.query import QuerySet

from dictionary.dictionary_apps.common.utils import (get_object)
from dictionary.dictionary_apps.words.filters import (WordFilter, NounFilter, VerbFilter,
                                                      ArticleFilter, LectionFilter,
                                                      AdjectiveFilter, NumeralFilter,
                                                      PronounFilter, NounDeclensionsFormFilter)
from dictionary.dictionary_apps.words.models import (Word, Lection, Article, Book,
                                                     Noun, WordType, Verb, Adjective,
                                                     Numeral, Pronoun, NounDeclensionsForm)


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

def numeral_get(numeral_id):
    numeral = get_object(Numeral, id=numeral_id)
    return  numeral

def numeral_list(*, filters=None):
    filters = filters or {}
    qs = Numeral.objects.all()
    return NumeralFilter(filters, qs).qs

def adjective_get(adjective_id):
    adjective = get_object(Adjective, id=adjective_id)
    return  adjective

def adjective_get_by_word(adjective_word):
    adjective = get_object(Adjective, word=adjective_word)
    return adjective
def adjective_list(*, filters=None):
    filters = filters or {}
    qs = Adjective.objects.all()
    return AdjectiveFilter(filters, qs).qs

def pronoun_get(pronoun_id):
    pronoun = get_object(Pronoun, id=pronoun_id)
    return  pronoun

def pronoun_list(*, filters=None):
    filters = filters or {}
    qs = Pronoun.objects.all()
    return PronounFilter(filters, qs).qs
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



def article_list(*, filters=None):
    filters = filters or {}
    qs = Article.objects.all()
    return ArticleFilter(filters, qs).qs



def lection_list(*, filters=None):
    filters = filters or {}
    qs = Lection.objects.all()
    return LectionFilter(filters, qs).qs


def noundecl_get(noundecl_id):
    noundecl = get_object(NounDeclensionsForm, id=noundecl_id)
    return  noundecl

def noundecl_list(*, filters=None):
    filters = filters or {}
    qs = NounDeclensionsForm.objects.all()
    return NounDeclensionsFormFilter(filters, qs).qs












































