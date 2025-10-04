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

from dictionary.dictionary_apps.users.selectors import (user_get)
from dictionary.dictionary_apps.users.models import BaseUser
from dictionary.dictionary_apps.words.models import Word
from dictionary.dictionary_apps.words.repository import WordRepository
from dictionary.dictionary_apps.words.services import WordService
from dictionary.dictionary_apps.dtos.words.request_dto import CreatePronounssExerciseDTO



case_dict = {
    'akkusativ': 'akkusativ_translate',
    'dativ': 'dativ_translate',
    'prossessive' : 'prossessive_translate',
    'reflexive': 'reflexive_translate',
}
def generate_exercise(pronouns=[]):
    # Получаем ID лекций из запроса
    exercises = []

    for pronoun in pronouns:
        case = random.choice([k for k in case_dict.keys()])
        case_translate = case_dict[case]
        answer = getattr(pronoun, case)
        question = getattr(pronoun, case)

        exercises.append(
            CreatePronounssExerciseDTO(
                pronoun=pronoun,
                case=case,
                case_name=case.capitalize(),
                correct_answer=answer,
            )
        )
    return exercises


class Pronouns(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'exercises/pronouns.html'

    def get(self, request):
        filters = {'word_type': 5}
        all_ids = list(Word.objects.filter(**filters).values_list('id', flat=True))
        if len(all_ids) >= 5:
            random_ids = random.sample(all_ids, 5)
        filters = {'id__in': random_ids}
        selected_words = WordService(WordRepository()).list_objects(filters)
        exercises = generate_exercise(pronouns=selected_words)
        context = {
            'exercises': exercises,
            'user': request.user,
        }
        return Response(context)

    def post(self, request):
        count = 5
        correct_count = 0
        results = []
        print(request.POST)
        for i in range(1, count + 1):
            user_input = request.POST.get(f"answer_{i}", "").strip().lower()
            correct_answer = request.POST.get(f"correct_{i}", "").strip().lower()
            is_correct = user_input == correct_answer
            pronoun = request.POST.get(f"pronoun_{i}", "").strip().lower()
            case = request.POST.get(f"case_{i}", "").strip().lower()
            results.append({
                "index": i,
                "user_input": user_input,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                'pronoun': pronoun,
                'case': case,
            })
            print(results)
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
            template_name='exercises/pronouns_results.html')


@csrf_exempt
@login_required
def pronouns_results_repeat(request):
    if request.method == "POST":
        points = int(request.POST.get("points", 0))
        lives_lost = int(request.POST.get("lives_lost", 0))
        user = request.user
        return redirect("api:exercises:pronouns")
    return HttpResponseBadRequest()


@csrf_exempt
@login_required
def pronouns_results_stop(request):
    if request.method == "POST":
        points = int(request.POST.get("points", 0))
        lives_lost = int(request.POST.get("lives_lost", 0))
        user = request.user
        return redirect("api:exercises:exercises_page")  # или на другую страницу
    return HttpResponseBadRequest()