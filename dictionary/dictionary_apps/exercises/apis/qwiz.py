import random

from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.renderers import TemplateHTMLRenderer


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

class TranslateWordPartQwiz():

    def __init__(self, dict_type_words):
        self.dict_type_words=dict_type_words

    def create(self, question='Как переводится это слово'):
        qwiz = {
            'question_word': '',
            'question': '',
            'variants': [],
            'richt_answer': '',
        }
        type_word = random.choice(list(self.dict_type_words.keys()))
        model = self.dict_type_words[str(type_word)]
        min_id, max_id = model.objects.aggregate(Min('id'), Max('id')).values()
        random_ids = set()
        while len(random_ids) < 3:
            random_id = random.randint(min_id, max_id)
            if model.objects.filter(id=random_id).exists():
                random_ids.add(random_id)
        random_words = list(model.objects.filter(id__in=random_ids))
        qwiz['variants'] = [w.word_translate for w in random_words]
        qwiz['question_word'] = random_words[0].word
        qwiz['question'] = f" {question} {qwiz['question_word']}?"
        random.shuffle(qwiz['variants'])
        qwiz['richt_answer'] = qwiz['variants'].index(random_words[0].word_translate)
        qwiz['richt_answer_value'] = qwiz['variants'][qwiz['richt_answer']]
        qwiz_str = (f"Как переводится это слово {qwiz['question_word']}? | {qwiz['variants'][0]} | "
                    f"{qwiz['variants'][1]} | {qwiz['variants'][2]} | {qwiz['richt_answer']}")
        print(qwiz_str)
        return qwiz

class NounArticlePartQwiz():

    def __init__(self, model):
        self.model = model

    def create(self, question = 'Какой артикль у слова'):
        print(question)
        min_id, max_id = self.model.objects.aggregate(Min('id'), Max('id')).values()
        qwiz_word = None
        qwiz = {
            'question_word':'',
            'question':'',
            'variants': [],
            'richt_answer': '',
        }
        while not qwiz_word:
            random_id = random.randint(min_id, max_id)
            if self.model.objects.filter(id=random_id).exists():
                qwiz_word =  self.model.objects.filter(id=random_id).first()
        print(qwiz_word, qwiz_word.article.name)
        qwiz['variants'] = ['der', 'die', 'das']
        qwiz['question'] = f"{question} {qwiz_word}?"
        qwiz['question_word'] = qwiz_word.word
        qwiz['richt_answer'] = qwiz['variants'].index(qwiz_word.article.name)
        qwiz['richt_answer_value'] = qwiz['variants'][qwiz['richt_answer']]

        qwiz_str = (f"Какой артикль у слова {qwiz['question_word']}? | {qwiz['variants'][0]} | "
                    f"{qwiz['variants'][1]} | {qwiz['variants'][2]} | {qwiz['richt_answer']}")
        print(qwiz_str)
        return qwiz


dict_type_qwiz = {
    '1': TranslateWordPartQwiz,
    '2': NounArticlePartQwiz,
}
class Qwiz(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'exercises/qwiz.html'

    # def __init__(self, questions):
    #     self.questions = questions
    def get(self, request):
        print('GET_QWIZ_LIST')
        limit = 10
        qwizes = []
        for i in range(limit):
            ch = random.choice(list(dict_type_qwiz.keys()))
            if ch == '1':
                temp_qwiz = TranslateWordPartQwiz(dict_type_words)
                qwiz_data = temp_qwiz.create()
                print(qwiz_data)
                qwizes.append(qwiz_data)
            elif ch == '2':
                temp_qwiz = NounArticlePartQwiz(Noun)
                qwiz_data = temp_qwiz.create()
                print(qwiz_data)
                qwizes.append(qwiz_data)
        print(qwizes)
        context = {
            'qwizes': qwizes
        }
        return Response(context)
