import random
import json

from django.http import Http404, JsonResponse
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from dictionary.dictionary_apps.words.models import Verb, Word
from dictionary.dictionary_apps.words.repository import WordRepository
from dictionary.dictionary_apps.words.services import WordService

from dictionary.dictionary_apps.dtos.words.request_dto import CreateExerciseDTO


PERSONS = [
    ("ich", "ich_form", "past_prateritum_ich_form"),
    ("du", "du_form", "past_prateritum_du_form"),
    ("er/sie/es", "er_sie_es_form", "past_prateritum_er_sie_es_form"),
    ("wir", "wir_form", "past_prateritum_wir_form"),
    ("ihr", "ihr_form", "past_prateritum_ihr_form"),
    ("Sie/sie", "Sie_sie_form", "past_prateritum_Sie_sie_form"),
]
def generate_exercise(tense=None, verbs=None, count=5):
    # Получаем ID лекций из запроса
    exercises = []
    selected_persons = random.choices(PERSONS, k=count)
    print(tense)
    for verb, (person, present_field, prateritum_field) in zip(verbs, selected_persons):
        if tense == "present":
            print('TENS', tense, verb.word, person)
            answer = getattr(verb, present_field)
            question = f"{verb.word} — {person}?"
            print(question, answer)
        elif tense == "prateritum":
            answer = getattr(verb, prateritum_field)
            question = f"{verb.word} в Präteritum — {person}?"
        elif tense == "perfect":
            answer = verb.past_perfect_form
            question = f"{verb.word} — Partizip II?"
    # else:
    #     continue
        exercises.append(
            CreateExerciseDTO(
                verb_id=verb.id,
                verb=verb.word,
                question=question,
                correct_answer=answer,
                person=person,
                tense=tense,
            )
        )
    return exercises


class VerbExercises(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'exercises/verb_forms.html'

    def get(self, request):
        lection_ids = request.GET.getlist('lections')
        tense = request.GET.get('tense')
        filters = {'word_type': 2}
        if lection_ids:
            filters['lection_id__in'] = lection_ids
        else:
            # Если ничего не выбрано — можно взять все
            pass  # или
        all_ids = list(Word.objects.filter(**filters).values_list('id', flat=True))
        if len(all_ids) >= 5:
            random_ids = random.sample(all_ids, 5)
        filters = {'id__in': random_ids}
        selected_words = WordService(WordRepository()).list_objects(filters)
        exercises = generate_exercise(tense=tense, verbs=selected_words)
        print('/TENSEGE', tense)
        context = {
            'exercises': exercises,
            'user': request.user,
            'limit': len(exercises),
            'lections': lection_ids,
            'tense': tense,
        }
        return Response(context)

    def post(self, request):
        #property_verb = request.GET.get('property_verb')
        lection_ids = request.POST.getlist('lections')
        tense = request.POST.get('tense')
        count = 5
        correct_count = 0
        results = []
        for i in range(1, count + 1):
            user_input = request.POST.get(f"answer_{i}", "").strip().lower()
            question = request.POST.get(f"question_{i}", "").strip().lower()
            correct_answer = request.POST.get(f"correct_{i}", "").strip().lower()
            is_correct = user_input == correct_answer


            results.append({
                "index": i,
                "user_input": user_input,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "question": question
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
        print('TENSEe', tense)
        return Response(
                {
                'results': results,
                'points': points,
                'lives_lost': lives_lost,
                'user': request.user,
                'tense': tense,
                'lections': lection_ids,
            },
            template_name='exercises/verb_results.html')





@csrf_exempt
@login_required
def verb_results_repeat(request):
    print('REQPOST', request.POST)
    if request.method == "POST":
        points = int(request.POST.get("points", 0))
        lives_lost = int(request.POST.get("lives_lost", 0))
        tense = str(request.POST.get('tense'))
        lection_ids = request.POST.getlist('lections')

        user = request.user
        # user.score += points
        # user.lifes = max(user.lifes - lives_lost, 0)
        # user.save()
        params = {'tense': tense}
        for l_id in lection_ids:
            params.setdefault('lections', []).append(l_id)
        url = reverse("api:exercises:exercises_verbs") + "?" + urlencode(params, doseq=True)
        return redirect(url)
        #return redirect("api:exercises:select_lections_verbs")
    return HttpResponseBadRequest()


@csrf_exempt
@login_required
def verb_results_stop(request):
    if request.method == "POST":
        points = int(request.POST.get("points", 0))
        lives_lost = int(request.POST.get("lives_lost", 0))

        user = request.user
        # user.score += points
        # user.lifes = max(user.lifes - lives_lost, 0)
        # user.save()

        return redirect("api:exercises:exercises_page")  # или на другую страницу
    return HttpResponseBadRequest()