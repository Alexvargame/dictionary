from dataclasses import dataclass
from typing import Optional
#from pydantic.dataclasses import dataclass
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

@dataclass
class LectionDTO:
    id: int
    name: str
    book: int
    description: str

@dataclass
class PronounDTO:
    id: Optional[int] = None
    word: Optional[str] = None
    word_translate: Optional[str] = None
    akkusativ: Optional[str] = None
    akkusativ_translate: Optional[str] = None
    dativ: Optional[str] = None
    dativ_translate: Optional[str] = None
    prossessive: Optional[str] = None
    prossessive_translate: Optional[str] = None
    reflexive: Optional[str] = None
    reflexive_translate: Optional[str] = None
    lection: Optional[int] = None
    word_type: Optional[int] = None

@dataclass
class NumeralDTO:
    id: Optional[int] = None
    word: Optional[str] = None
    word_translate: Optional[str] = None
    ordinal: Optional[str] = None
    date_numeral: Optional[str] = None
    lection: Optional[int] = None
    word_type: Optional[int] = None
@dataclass
class AdjectiveDTO:
    id: Optional[int] = None
    word: Optional[str] = None
    word_translate: Optional[str] = None
    komparativ: Optional[str] = None
    superlativ: Optional[str] = None
    declensions: Optional[str] = None
    lection: Optional[int] = None
    word_type: Optional[int] = None

@dataclass
class NounDeclensionsFormDTO:
    id: int
    noun: int
    nominativ: str
    akkusativ: str
    dativ: str
    genitiv: str
    plural_nominativ: str
    plural_akkusativ: str
    plural_dativ: str
    plural_genitiv: str