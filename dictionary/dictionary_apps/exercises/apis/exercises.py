from django.shortcuts import render

from dictionary.dictionary_apps.words.models import Lection
from dictionary.dictionary_apps.words.repository import LectionRepository
from dictionary.dictionary_apps.words.services import LectionService
def exercises_page(request):

    return render(request, 'exercises/exercises.html')


def select_lections_ordering_words(request):
    #lections = Lection.objects.all()
    lections = LectionService(LectionRepository()).list_objects()
    context = {
        'lections': lections
    }
    return render(request, 'exercises/select_lection_ordering_words.html', context=context)

def select_lections_article_words(request):
    lections = LectionService(LectionRepository()).list_objects()
    context = {
        'lections': lections
    }
    return render(request, 'exercises/select_lection_article_words.html', context=context)

def select_lections_verbs(request):
    lections = LectionService(LectionRepository()).list_objects()
    context = {
        'lections': lections
    }
    return render(request, 'exercises/select_lection_verbs.html', context=context)


def select_lections_adjectivs(request):
    lections = LectionService(LectionRepository()).list_objects()
    context = {
        'lections': lections
    }
    return render(request, 'exercises/select_lection_adjectivs.html', context=context)