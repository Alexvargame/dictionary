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
from dictionary.dictionary_apps.dtos.words.request_dto import CreateDigitsExerciseDTO



units = {
    1: "ein", 2: "zwei", 3: "drei", 4: "vier", 5: "fünf",
    6: "sechs", 7: "sieben", 8: "acht", 9: "neun"
}

teens = {
    10: "zehn", 11: "elf", 12: "zwölf", 13: "dreizehn",
    14: "vierzehn", 15: "fünfzehn", 16: "sechzehn",
    17: "siebzehn", 18: "achtzehn", 19: "neunzehn"
}

tens = {
    20: "zwanzig", 30: "dreißig", 40: "vierzig",
    50: "fünfzig", 60: "sechzig", 70: "siebzig",
    80: "achtzig", 90: "neunzig"
}

def number_to_german(n):
    if n == 0:
        return "null"
    elif n <= 12:
        return {
            1: "eins", 2: "zwei", 3: "drei", 4: "vier",
            5: "fünf", 6: "sechs", 7: "sieben", 8: "acht",
            9: "neun", 10: "zehn", 11: "elf", 12: "zwölf"
        }[n]
    elif 13 <= n <= 19:
        return teens[n]
    elif n < 100:
        unit = n % 10
        ten = n - unit
        if unit == 0:
            return tens[ten]
        return f"{units[unit]}und{tens[ten]}"
    elif 100 <= n < 1000:
        unit = n % 10
        ten = n % 100 - unit
        hundred = n // 100
        print('afwe', unit, ten, hundred)
        if 9 < ten < 20:
            if unit == 0:
                return f"{units[hundred]} hundert {teens[ten]}"
            else:
                return f"{units[hundred]} hundert {teens[ten + unit]}"

        if unit == 0:
            return f"{units[hundred]} hundert {tens[ten]}"
        if ten == 0:
            return f"{units[hundred]} hundert {units[unit]}"
        return f"{units[hundred]} hundert {units[unit]}und{tens[ten]}"
    else:
        return "nicht unterstützt"  # >1000 пока не поддерживаем
def generate_exercise(digits=[]):
    # Получаем ID лекций из запроса
    exercises = []
    for digit in digits:
        answer = number_to_german(digit)
        exercises.append(
            CreateDigitsExerciseDTO(
                digit=digit,
                correct_answer=answer,
            )
        )
    return exercises


class Digits(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'exercises/digits.html'

    def get(self, request):
        random_numbers = random.sample(range(1, 1001), 5)
        exercises = generate_exercise(digits=random_numbers)
        context = {
            'exercises': exercises,
            'user': request.user,
        }
        return Response(context)

    def post(self, request):
        print('POSTDIGTY')
        count = 5
        correct_count = 0
        results = []
        for i in range(1, count + 1):
            user_input = request.POST.get(f"answer_{i}", "").strip().lower()
            correct_answer = request.POST.get(f"correct_{i}", "").strip().lower()
            is_correct = user_input == correct_answer
            digit = request.POST.get(f"digit_{i}", "").strip().lower()
            results.append({
                "index": i,
                "user_input": user_input,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                'digit': digit,
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
            template_name='exercises/digits_results.html')


@csrf_exempt
@login_required
def digits_results_repeat(request):
    if request.method == "POST":
        points = int(request.POST.get("points", 0))
        lives_lost = int(request.POST.get("lives_lost", 0))
        user = request.user
        return redirect("api:exercises:digits")
    return HttpResponseBadRequest()


@csrf_exempt
@login_required
def digits_results_stop(request):
    if request.method == "POST":
        points = int(request.POST.get("points", 0))
        lives_lost = int(request.POST.get("lives_lost", 0))
        user = request.user
        return redirect("api:exercises:exercises_page")  # или на другую страницу
    return HttpResponseBadRequest()