from django.shortcuts import render

from dictionary.dictionary_apps.words.models import Lection
def exercises_page(request):

    return render(request, 'exercises/exercises.html')


def select_lections_ordering_words(request):
    lections = Lection.objects.all()
    context = {
        'lections': lections
    }
    return render(request, 'exercises/select_lection_ordering_words.html', context=context)

def select_lections_verbs(request):
    lections = Lection.objects.all()
    context = {
        'lections': lections
    }
    return render(request, 'exercises/select_lection_verbs.html', context=context)