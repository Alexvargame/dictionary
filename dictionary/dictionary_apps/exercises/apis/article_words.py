import random
import json

from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt  # если нет CSRF токена в fetch, но лучше с ним


from dictionary.dictionary_apps.words.models import Noun

from dictionary.dictionary_apps.words.selectors import (lection_get, article_get,
                                                        word_get)
from dictionary.dictionary_apps.users.selectors import (user_get)

#from worterbuch.worterbuch_apps.dtos.words.response_dto import WordDTO
from dictionary.dictionary_apps.words.services import WordService, ArticleService
from dictionary.dictionary_apps.words.repository import WordRepository, ArticleRepository

from dictionary.dictionary_apps.users.models import BaseUser

from dictionary.dictionary_apps.dtos.words.response_dto import (NounPaarExerciseGermanDTO, VerbPaarExerciseGermanDTO,
                                                                RussianPaarExerciseGermanDTO)



class ArticleNouns(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'exercises/article_words.html'

    def get(self, request):

        result_list = []
        lection_ids = request.GET.getlist('lections')  # Получаем ID лекций из запроса
        filters = {}
        if lection_ids:
            filters['lection_id__in'] = lection_ids
        else:
            # Если ничего не выбрано — можно взять все
            pass  # или

        all_ids = list(Noun.objects.filter(**filters).values_list('id', flat=True))
        if len(all_ids) >= 5:
            random_ids = random.sample(all_ids, 5)
        filters = {'id__in': random_ids}
        selected_words = WordService(WordRepository()).list_objects(filters)
        for word in selected_words:
            result_list.append(
                NounPaarExerciseGermanDTO(
                    **{'id': word.id, 'article': word.article.name,
                       'word': word.word, 'word_type': word.word_type}
                )
            )
        articles = ArticleService(ArticleRepository()).list_objects()
        context = {
            'result_list': result_list,
            'user': request.user,
            'limit': len(result_list),
            'articles': articles
        }
        return Response(context)

    def post(self, request):
        count = 5
        correct_count = 0
        results = []
        for i in range(1, count + 1):
            user_input = request.POST.get(f"answer_{i}", "").strip().lower()
            correct_answer = request.POST.get(f"correct_{i}", "").strip().lower()
            is_correct = user_input == correct_answer
            word = request.POST.get(f"word_{i}", "").strip().lower()

            results.append({
                "index": i,
                "user_input": user_input,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "word": word,
            })

            if is_correct:
                correct_count += 1
        points = correct_count
        lives_lost = 1 if correct_count < count else 0

        if request.user.is_authenticated:
            user = request.user
            user.score += points
            user.lifes = max(user.lifes - lives_lost, 0)
            user.save()

        return Response(
            {
                'results': results,
                'points': points,
                'lives_lost': lives_lost,
                'user': request.user,
            },
            template_name='exercises/article_results.html')


@csrf_exempt
@login_required
def article_results_repeat(request):
    if request.method == "POST":
        points = int(request.POST.get("points", 0))
        lives_lost = int(request.POST.get("lives_lost", 0))

        user = request.user
        user.score += points
        user.lifes = max(user.lifes - lives_lost, 0)
        user.save()

        return redirect("api:exercises:select_lections_article_words")
    return HttpResponseBadRequest()


@csrf_exempt
@login_required
def article_results_stop(request):
    if request.method == "POST":
        points = int(request.POST.get("points", 0))
        lives_lost = int(request.POST.get("lives_lost", 0))

        user = request.user
        user.score += points
        user.lifes = max(user.lifes - lives_lost, 0)
        user.save()

        return redirect("api:exercises:exercises_page")  # или на другую страницу
    return HttpResponseBadRequest()