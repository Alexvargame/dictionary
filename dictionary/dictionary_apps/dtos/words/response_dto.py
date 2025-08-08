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
    past_perfect_form: str
    past_prateritum_ich_form: str
    past_prateritum_du_form: str
    past_prateritum_er_sie_es_form: str
    past_prateritum_wir_form: str
    past_prateritum_ihr_form: str
    past_prateritum_Sie_sie_form: str
    lection: Lection
    word_type: WordType

@dataclass
class NounPaarExerciseGermanDTO:
    id: int
    word: str
    article: str
    word_type: str

@dataclass
class VerbPaarExerciseGermanDTO:
    id: int
    word: str
    article: str
    word_type: str

@dataclass
class RussianPaarExerciseGermanDTO:
    id: int
    word_translate: str

@dataclass
class ArticleDTO:
    id: int
    name: str
    description: str