import random
from django.db.models import Min, Max



from dictionary.dictionary_apps.words.models import (Noun, Verb, Adjective,
                                                     Pronoun, OtherWords)
from dictionary.dictionary_apps.exercises.apis.digits import number_to_german, units, tens, teens


dict_type_words = {
    '1': Noun,
    '2': Verb,
    '3': Adjective,
    '4': Pronoun,
    '5': OtherWords,
}

class TranslateWordQwiz():

    def __init__(self, dict_type_words):
        self.dict_type_words=dict_type_words

    def create(self):

        type_word = random.choice(list(self.dict_type_words.keys()))
        model = self.dict_type_words[str(type_word)]
        min_id, max_id = self.model.objects.aggregate(Min('id'), Max('id')).values()
        random_ids = set()
        while len(random_ids) < 3:
            random_id = random.randint(min_id, max_id)
            if model.objects.filter(id=random_id).exists():
                random_ids.add(random_id)
        random_words = list(model.objects.filter(id__in=random_ids))
        answer_words = [w.word_translate for w in random_words]
        question_word = random_words[0].word
        random.shuffle(answer_words)
        richt_answer = answer_words.index(random_words[0].word_translate)
        qwiz_str = (f"Как переводится это слово {question_word}? | {answer_words[0]} | "
                    f"{answer_words[1]} | {answer_words[2]} | {richt_answer}")
        return qwiz_str

class NounArticleQwiz():

    def __init__(self, model):
        self.model = model
    def create(self):
        min_id, max_id = self.model.objects.aggregate(Min('id'), Max('id')).values()
        qwiz_word = None
        while not qwiz_word:
            random_id = random.randint(min_id, max_id)
            if self.model.objects.filter(id=random_id).exists():
                qwiz_word =  self.model.objects.filter(id=random_id).first()
        print(qwiz_word, qwiz_word.article.name)
        answer_words = ['der', 'die', 'das']
        question_word = qwiz_word.word
        richt_answer = answer_words.index(qwiz_word.article.name)
        qwiz_str = (f"Какой артикль у слова {question_word}? | {answer_words[0]} | "
                    f"{answer_words[1]} | {answer_words[2]} | {richt_answer}")

        return qwiz_str

class TranslateNumeralQwiz():

    def __init__(self):
        pass
    def create(self):
        digit = random.randint(0, 999)
        digit_in_german = number_to_german(digit)
        print(digit, digit_in_german)
        varinats = set()
        varinats.add(digit)
        while len(varinats) <3:
            tmp_digit = random.randint(0,999)
            varinats.add(tmp_digit)
        print(varinats)
        answer_words = list(varinats)
        question_word = digit_in_german
        richt_answer = answer_words.index(digit)
        qwiz_str = (f"Какое это число  {question_word}? | {answer_words[0]} | "
                    f"{answer_words[1]} | {answer_words[2]} | {richt_answer}")

        return qwiz_str

















