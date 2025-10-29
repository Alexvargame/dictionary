import random
from django.db.models import Min, Max



from dictionary.dictionary_apps.words.models import (Noun, Verb, Adjective,
                                                     Pronoun, OtherWords)

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
        print(model)
        min_id, max_id = model.objects.aggregate(Min('id'), Max('id')).values()

        random_ids = set()
        while len(random_ids) < 3:
            random_id = random.randint(min_id, max_id)
            if model.objects.filter(id=random_id).exists():
                random_ids.add(random_id)
        random_words = list(model.objects.filter(id__in=random_ids))
        print(random_words)
        answer_words = [w.word_translate for w in random_words]
        print(answer_words)
        question_word = random_words[0].word
        random.shuffle(answer_words)
        print(answer_words)
        richt_answer = answer_words.index(random_words[0].word_translate)
        print(richt_answer)

        print(random_words)
        qwiz_str = (f"Как переводится это слово {question_word}? | {answer_words[0]} | "
                    f"{answer_words[1]} | {answer_words[2]} | {richt_answer}")

        print(qwiz_str)

        return qwiz_str



















