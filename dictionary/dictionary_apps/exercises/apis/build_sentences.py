import random

from django.http import Http404, JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from dictionary.dictionary_apps.words.models import SentenceBuild



class BuildSentences(LoginRequiredMixin, APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'exercises/build_sentences.html'

    def get(self, request):

        all_ids = [object.id for object in SentenceBuild.objects.all()]
        if not all_ids:
            return Response({'error': 'Нет предложений'}, status=404)
        idx = random.choice(all_ids)
        sentence = get_object_or_404(SentenceBuild, id=idx)
        words = [w.strip(',.!?') for w in sentence.text.split(' ')]
        random.shuffle(words)
        print(words, sentence)
        context = {
            'words': words,
            'user': request.user,
            'sentence_id': sentence.id
        }
        return Response(context)


    def post(self, request):
        print(request.data)
        sentence_id = request.data.get('sentence_id')
        print(sentence_id, type(sentence_id))
        user_words = request.data.get('words')
        sentence = get_object_or_404(SentenceBuild, id=int(sentence_id))
        check_words = [word.strip(',.!?') for word in sentence.text.split()]

        is_correct = (check_words == check_words)
        print('СОВПАДЛО?', is_correct)
        is_correct = (user_words == check_words)

        # Собираем данные в точности как в твоем шаблоне с числительными
        results = [{
            'index': 1,
            'numeral': sentence.text,  # (в шаблоне выведется как задание)
            'user_input': ' '.join(user_words),
            'is_correct': is_correct,
            'correct_answer': sentence.text,
            'translate': sentence.translate,
            'comment': sentence.comment
        }]
        if is_correct:
            points = 1
            lives_lost = 0
        else:
            points = 0
            lives_lost = 1

        if request.user.is_authenticated:
            user = request.user
            user.score += points
            user.lifes = max(user.lifes - lives_lost, 0)
            user.save()
        context = {
            'results': results,
            'points': points,
            'lives_lost': lives_lost,
            'user': request.user,
        }
        # Отдаем HTML-страницу с результатами
        return Response(context, template_name='exercises/sentences_results.html')
        # (Укажи правильный путь к своему шаблону результатов)

@csrf_exempt
@login_required
def sentences_results_repeat(request):
    if request.method == "POST":
        # points = int(request.POST.get("points", 0)) # если нужно
        return redirect("api:exercises:build_sentences") # <-- имя URL твоего упражнения
    return HttpResponseBadRequest()


@csrf_exempt
@login_required
def sentences_results_stop(request):
    if request.method == "POST":
        return redirect("api:exercises:exercises_page") # <-- обратно в меню
    return HttpResponseBadRequest()