from dataclasses import dataclass
from typing import Optional

from dictionary.dictionary_apps.words.models import Word, Lection, Article, WordType



@dataclass
class CreateWordDTO:

    word_type: WordType
    lection: Lection

@dataclass
class CreateNounDTO:

    word: str
    word_plural: str
    plural_sign: str
    word_translate: str
    word_translate_plural: str
    article: Article
    lection: Lection
    word_type: WordType

@dataclass
class CreateVerbDTO:
    word: str
    word_translate: str
    ich_form: str
    du_form: str
    er_sie_es_form: str
    wir_form: str
    ihr_form: str
    Sie_sie_form: str
    lection: Lection
    word_type: WordType
    past_perfect_form: Optional[str] = None
    past_prateritum_ich_form: Optional[str] = None
    past_prateritum_du_form: Optional[str] = None
    past_prateritum_er_sie_es_form: Optional[str] = None
    past_prateritum_wir_form: Optional[str] = None
    past_prateritum_ihr_form: Optional[str] = None
    past_prateritum_Sie_sie_form: Optional[str] = None


@dataclass
class CreateExerciseDTO:
    verb_id: int
    verb: str
    question: str
    correct_answer: str
    person: str
    tense: str
