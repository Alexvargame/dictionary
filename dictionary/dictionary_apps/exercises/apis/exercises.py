from django.shortcuts import render
from django.db.models import Count, Q

from dictionary.dictionary_apps.words.models import Lection
from dictionary.dictionary_apps.words.repository import LectionRepository
from dictionary.dictionary_apps.words.services import LectionService
def exercises_page(request):

    return render(request, 'exercises/exercises.html')


def get_lections_for_wordtype(word_type_id: int):
    return (
        Lection.objects
        .annotate(word_count=Count("lection", filter=Q(lection__word_type_id=word_type_id)))
        .filter(word_count__gt=0)
    )


def select_lections_ordering_words(request):
    #lections = Lection.objects.all()
    lections = LectionService(LectionRepository()).list_objects()
    context = {
        'lections': lections
    }
    return render(request, 'exercises/select_lection_ordering_words.html', context=context)

def select_lections_article_words(request):
    lections = get_lections_for_wordtype(1)
    context = {
        'lections': lections
    }
    return render(request, 'exercises/select_lection_article_words.html', context=context)

def select_lections_verbs(request):
    lections = get_lections_for_wordtype(2)
    context = {
        'lections': lections
    }
    return render(request, 'exercises/select_lection_verbs.html', context=context)



def select_lections_adjectivs(request):
    lections = get_lections_for_wordtype(3)
    context = {
        'lections': lections
    }
    return render(request, 'exercises/select_lection_adjectivs.html', context=context)
