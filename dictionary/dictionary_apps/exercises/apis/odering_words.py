import random
import json

from django.http import Http404, JsonResponse
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt  # если нет CSRF токена в fetch, но лучше с ним


from dictionary.dictionary_apps.words.models import Word, Noun, Verb

from dictionary.dictionary_apps.words.selectors import (lection_get, article_get,
                                                        word_get)
from dictionary.dictionary_apps.users.selectors import (user_get)

#from worterbuch.worterbuch_apps.dtos.words.response_dto import WordDTO
from dictionary.dictionary_apps.words.services import WordService
from dictionary.dictionary_apps.words.repository import WordRepository

from dictionary.dictionary_apps.users.models import BaseUser

# class OrderingWordsDRF(LoginRequiredMixin, APIView):
#     class OutputSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = Word
#             fields = ('id', 'id', 'word_single', 'word_plural', 'word_translate',
#                     'word_translate_plural','lection', 'article')
#     def get(self, request):
#
#         all_ids = list (Word.objects.values_list('id', flat=True))
#         if len(all_ids) >= 5:
#             random_ids = random.sample(all_ids, 5)
#         #     random_objects = Word.objects.filter(id__in=random_ids)
#         # print(random_objects)
#         filters = {'id': random_ids}
#         selected_words = WordService(WordRepository()).list_objects(filters)
#         german_list = [word.word_single for word in selected_words]
#         russian_list = [word.word_translate for word in selected_words]
#         print(german_list, russian_list)
#         random.shuffle(german_list)
#         random.shuffle(russian_list)
#         print(german_list, russian_list)
#         data = self.OutputSerializer(selected_words)
#         return Response(data)



class OrderingWords(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'exercises/ordering_words.html'

    def get(self, request):
        german_list = []
        russian_list = []
        all_ids = list(Word.objects.values_list('id', flat=True))
        print('iDS', all_ids)
        if len(all_ids) >= 5:
            random_ids = random.sample(all_ids, 5)
        filters = {'id__in': random_ids}
        selected_words = WordService(WordRepository()).list_objects(filters)
        for word in selected_words:
            if word.word_type.name == 'Noun':
                german_list.append({
                            'id': word.id,
                            'article': word.article.name,
                            'word': word.word,
                            'type': 'Noun'}
                            )
                russian_list.append({
                    'id':word.id,
                    'word_translate':word.word_translate
                })
            elif word.word_type.name == 'Verb':
                german_list.append({
                                'id': word.id,
                                'article': '',
                                'word': word.word,
                                'type': 'Verb'}
                            )
                russian_list.append(
                    {
                        'id': word.id,
                        'word_translate': word.word_translate
                    }
                )
        random.shuffle(german_list)
        random.shuffle(russian_list)
        context = {
            'german_list': german_list,
            'russian_list': russian_list,
            'user': request.user,
            'limit': len(german_list)
        }
        return Response(context)

@login_required
@csrf_exempt  # временно, если не используешь CSRF токен в fetch
def save_progress(request):
    print('TOKEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEee')
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            score = data.get('score')
            lifes = data.get('lifes')
            user = request.user
            # Для проверки просто выведем в консоль
            print(f"Получено с клиента {user}: score={score}, lifes={lifes}")

            # TODO: тут можно сохранить данные в базу, обновить пользователя и т.п.
            if lifes is not None:
                user.lifes = lifes
            if score is not None:
                user.score += score
            print(user.lifes, user.score)
            user.save()
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            print("Ошибка обработки данных:", e)
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Только POST'}, status=405)