import random
import json

from django.http import Http404, JsonResponse
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import redirect, render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from dictionary.dictionary_apps.words.models import Adjective, Word, NounDeclensionsForm
from dictionary.dictionary_apps.words.repository import WordRepository
from dictionary.dictionary_apps.words.services import WordService

from dictionary.dictionary_apps.dtos.words.request_dto import CreateExerciseAdjectivDTO, CreateexerciseCasusAdjectiveDTO

from dictionary.dictionary_apps.words.selectors import adjective_get_by_word, noundecl_get

from .dictionarys import *

def get_all_values(d):
    values = []
    for v in d.values():
        if isinstance(v, dict):
            values.extend(get_all_values(v))
        else:
            values.append(v)
    return values


def get_declined_form(noun, case: str, number: str = "Plural"):
    if number == "Plural":
        field_name = f"plural_{case.lower()}"
    else:
        field_name = case.lower()  # nominativ, genitiv и т.д.
    return getattr(noun, field_name, None)

def generate_exercise(property_adjective=None, adjectivs=None, count=5):
    # Получаем ID лекций из запроса
    exercises = []

    print('SSSSSSSSSSSS', property_adjective)

    if property_adjective == "komparativ_und_superlativ":
        selected_degrees = random.choices(degrees_of_comparison, k=count)
        for adj, degree in zip(adjectivs, selected_degrees):
            answer = getattr(adj, degree)
            question = f"{adj.word} — {degree}?"
            exercises.append(
                CreateExerciseAdjectivDTO(
                    adjective_id=adj.id,
                    adjective=adj.word,
                    question=question,
                    correct_answer=answer,
                    # degree=degree,
                    property_adjective=property_adjective,
                )
            )
    elif property_adjective == "declensions":
        selected_declensions = random.choices(declensions, k=count)
        selected_cases = random.choices(cases, k=count)
        selected_genders = random.choices(list(gender.values()), k=count)
        for adj, decl, case, gender_dict in list(zip(adjectivs, selected_declensions, selected_cases, selected_genders)):
            gender_name, article = list(gender_dict.items())[0]
            print('PPPPPPP', decl,case,gender_name, article)
            print(adj.declensions[decl][case][gender_name][article])
            answer = adj.declensions[decl][case][gender_name][article]
            question = f"{adj.word} в Склонение: {decl}, Падеж: {case}, Род: {gender_name}, Артикль: {article}?"
            exercises.append(
                CreateExerciseAdjectivDTO(
                    adjective_id=adj.id,
                    adjective=adj.word,
                    question=question,
                    correct_answer=answer,
                    # degree=degree,
                    property_adjective=property_adjective,
                )
            )
    elif property_adjective == "casus":
        all_ids = list(NounDeclensionsForm.objects.values_list('id', flat=True))
        if len(all_ids) >= 0:
            random_id = random.sample(all_ids, 1)[0]
        noun = noundecl_get(random_id)
        print('NOUN', noun.noun.word, noun.noun.article.name, noun.noun.plural_sign)
        if noun.noun.plural_sign == 'nan':
            gender = 'Plural'
            noun_article = 'die'
            noun_question = noun.noun.word
            print('NIOUN_Forn_1', gender, noun_article)
        else:
            if random.choice(["Singular", "Plural"]) == 'Plural':
                gender = 'Plural'
                noun_article = 'die'
                noun_question = noun.noun.word_plural
                print('NIOUN_Forn_2', gender, noun_article, noun.noun.word_plural)
            else:
                gender = articles[noun.noun.article.name]
                noun_article = noun.noun.article.name
                noun_question = noun.noun.word
                print('NIOUN_Forn_3', gender, noun_article)

        adj = adjectivs[0]
        if gender == 'Plural':
            article = random.choice(['definite', 'kein'])
        else:
            article = random.choice(['definite', 'ein'])
        answer = ''
        cases = random.choice(cases_choice)
        print('RESULTTTSS', gender, article, noun_article, noun_question, cases)
        if gender == 'Plural':
            if article != 'definite':
                article_answer = [c for c in adj.declensions['stark'][cases][gender].keys() if c[0] == 'k'][0]
            else:
                article_answer = [c for c in adj.declensions['stark'][cases][gender].keys() if c[0] == 'd'][0]
        else:
            if article != 'definite':
                article_answer = [c for c in adj.declensions['stark'][cases][gender].keys() if c[0] == 'e'][0]
            else:
                article_answer = [c for c in adj.declensions['stark'][cases][gender].keys() if c[0] == 'd'][0]

        for key in adj.declensions['stark'][cases][gender].keys():
            if key in casus_articles[article]:
                answer = key
                break
        noun_answer = get_declined_form(noun, cases, gender)
        print('NOIUNANS', noun_answer)
        answer_parts = {
            "article": article_answer,
            "adj": adj.declensions['stark'][cases][gender][article_answer],
            "noun": noun_answer
        }
        print("AHSWR", answer_parts)
        noun_forms = [
            getattr(noun, field)
            for field in [
                "nominativ", "genitiv", "dativ", "akkusativ",
                "plural_nominativ", "plural_genitiv", "plural_dativ", "plural_akkusativ"
            ]
            if getattr(noun, field)
        ]
        exercises.append(
            CreateexerciseCasusAdjectiveDTO(
            article=article,
            article_forms=list(set(casus_articles[article])),
            adj=adj.id,
            adj_forms=list(set(get_all_values(adj.declensions))),
            noun=noun.noun.word,
            noun_forms=list(set(noun_forms)),
            answer=answer_parts,
            question=f" {article} {adj.word} {noun_question} {cases}",
        )
    )
    return exercises


class AdjectiveExercises(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'exercises/adjective_forms.html'

    def get(self, request):
        print(request.GET)
        lection_ids = request.GET.getlist('lections')
        property_adjective = request.GET.get('property_adjective')
        filters = {'word_type': 3}
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
        print('RAN', random_ids, 'select', selected_words)
        exercises = generate_exercise(property_adjective=property_adjective, adjectivs=selected_words)
        print('eXErs', exercises)
        context = {
            'exercises': exercises,
            'user': request.user,
            'limit': len(exercises)
        }
        return Response(context)

    def post(self, request):
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

        return Response(
                {
                'results': results,
                'points': points,
                'lives_lost': lives_lost,
                'user': request.user,
            },
            template_name='exercises/adjective_results.html')

class AdjectiveCasusExercises(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'exercises/adjective_casus.html'

    def get(self, request):
        property_adjective = request.GET.get('property_adjective')
        filters = {'word_type': 3}
        all_ids = list(Word.objects.filter(**filters).values_list('id', flat=True))
        if len(all_ids) >= 0:
            random_ids = random.sample(all_ids, 1)
        filters = {'id__in': random_ids}
        selected_words = WordService(WordRepository()).list_objects(filters)
        exercises = generate_exercise(property_adjective=property_adjective, adjectivs=selected_words)
        print('eXErs', exercises)
        context = {
            'exercises': exercises[0],
            'user': request.user,
            'limit': len(exercises)
        }
        return Response(context)

    def post(self, request):
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

        return Response(
                {
                'results': results,
                'points': points,
                'lives_lost': lives_lost,
                'user': request.user,
            },
            template_name='exercises/adjective_results.html')

class AdjectiveExercisesRepeat(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'exercises/adjective_forms.html'

    def post(self, request):
        # Получаем POST данные
        property_adjective = request.POST.get('property_adjective', 'komparativ_und_superlativ')
        points = int(request.POST.get('points', 0))
        lives_lost = int(request.POST.get('lives_lost', 0))

        # Обновляем пользователя
        user = request.user
        user.score += points
        user.lifes = max(user.lifes - lives_lost, 0)
        user.save()

        # Берём слова того же типа (Adjective)
        filters = {'word_type': 3}  # 3 = Adjective
        all_ids = list(Word.objects.filter(**filters).values_list('id', flat=True))
        random_ids = random.sample(all_ids, 5) if len(all_ids) >= 5 else all_ids
        selected_words = WordService(WordRepository()).list_objects({'id__in': random_ids})

        # Генерируем упражнения
        exercises = generate_exercise(property_adjective=property_adjective, adjectivs=selected_words)

        # Контекст для шаблона
        context = {
            'exercises': exercises,
            'user': request.user,
            'limit': len(exercises),
            'property_adjective': property_adjective
        }

        return Response(context, template_name='exercises/adjective_results.html')

@csrf_exempt
@login_required
def adjectivs_results_repeat(request):
    if request.method == "POST":
        points = int(request.POST.get("points", 0))
        lives_lost = int(request.POST.get("lives_lost", 0))

        user = request.user
        user.score += points
        user.lifes = max(user.lifes - lives_lost, 0)
        user.save()
        return redirect("api:exercises:select_lections_adjectivs")
    return HttpResponseBadRequest()


@csrf_exempt
@login_required
def adjectivs_results_stop(request):
    if request.method == "POST":
        points = int(request.POST.get("points", 0))
        lives_lost = int(request.POST.get("lives_lost", 0))

        user = request.user
        user.score += points
        user.lifes = max(user.lifes - lives_lost, 0)
        user.save()

        return redirect("api:exercises:exercises_page")  # или на другую страницу
    return HttpResponseBadRequest()