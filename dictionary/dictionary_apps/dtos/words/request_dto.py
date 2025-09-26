from dataclasses import dataclass
from typing import Optional, List
#from pydantic.dataclasses import dataclass

from dictionary.dictionary_apps.words.models import Word, Lection, Article, WordType



@dataclass
class CreateWordDTO:

    word_type: WordType
    lection: Lection

@dataclass
class CreateNounDTO:

    word: str
    word_type: int
    word_plural: Optional[str] = None
    plural_sign: Optional[str] = None
    word_translate: Optional[str] = None
    word_translate_plural: Optional[str] = None
    article: Optional[int] = None
    lection: Optional[int] = None


@dataclass
class CreateVerbDTO:
    word: str
    word_type: int
    word_translate: Optional[str] = None
    ich_form: Optional[str] = None
    du_form: Optional[str] = None
    er_sie_es_form: Optional[str] = None
    wir_form: Optional[str] = None
    ihr_form: Optional[str] = None
    Sie_sie_form: Optional[str] = None
    lection: Optional[int] = None
    past_perfect_form: Optional[str] = None
    past_prateritum_ich_form: Optional[str] = None
    past_prateritum_du_form: Optional[str] = None
    past_prateritum_er_sie_es_form: Optional[str] = None
    past_prateritum_wir_form: Optional[str] = None
    past_prateritum_ihr_form: Optional[str] = None
    past_prateritum_Sie_sie_form: Optional[str] = None

@dataclass
class CreatePronounDTO:
    word: str
    word_type: int
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

@dataclass
class CreateNumeralDTO:
    word: str
    word_type: int
    word_translate: Optional[str] = None
    ordinal: Optional[str] = None
    date_numeral: Optional[str] = None
    lection: Optional[int] = None

@dataclass
class CreateAdjectiveDTO:
    word: str
    word_type: int
    word_translate: Optional[str] = None
    komparativ: Optional[str] = None
    superlativ: Optional[str] = None
    declensions: Optional[str] = None
    lection: Optional[int] = None
@dataclass
class CreateExerciseDTO:
    verb_id: int
    verb: str
    question: str
    correct_answer: str
    person: str
    tense: str

@dataclass
class CreateDigitsExerciseDTO:

    digit: int
    correct_answer: str

@dataclass
class CreatePronounssExerciseDTO:

    pronoun: int
    case: str
    case_name: str
    correct_answer: str

@dataclass
class CreateNumeralsExerciseDTO:

    numeral: int
    field: str
    field_translate: str
    correct_answer: str


@dataclass
class CreateExerciseAdjectivDTO:
    adjective_id: int
    adjective: str
    question: str
    correct_answer: str
    # degree: str
    property_adjective: str

@dataclass
class CreateexerciseCasusAdjectiveDTO:
    article: str
    article_forms: List
    adj: int
    adj_forms: List
    noun: str
    noun_forms: List
    answer: dict
    question: str