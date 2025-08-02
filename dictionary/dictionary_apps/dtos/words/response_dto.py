from dataclasses import dataclass

from dictionary.dictionary_apps.words.models import Word, Article, Book, Lection, WordType

@dataclass
class WordDTO:
    id: int
    lection: Lection
    word_type: WordType

@dataclass
class NounDTO:
    id: int
    word: str
    word_plural: str
    plural_sign: str
    word_translate: str
    word_translate_plural: str
    article: Article
    lection: Lection
    word_type: WordType

@dataclass
class VerbDTO:
    id: int
    word: str
    word_translate: str
    ich_form: str
    du_form: str
    er_sie_es_form: str
    wir_form: str
    ihr_form: str
    Sie_sie_form: str
    past_prefect_form: str
    past_pretorium_ich_form: str
    past_pretorium_du_form: str
    past_pretorium_er_sie_es_form: str
    past_pretorium_wir_form: str
    past_pretorium_ihr_form: str
    past_pretorium_Sie_sie_form: str
    lection: Lection
    word_type: WordType