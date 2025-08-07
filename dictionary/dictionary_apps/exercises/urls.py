from django.urls import path
#
# from .apis import (NounCreateApi, NounDetailApi, NounListApi,
#                         NounDeleteApi, NounUpdateApi,
#                   )
from .apis.odering_words import OrderingWords, save_progress
from .apis.verbs_exercises import VerbExercises, verb_results_stop, verb_results_repeat
from .apis.exercises import (exercises_page, select_lections_ordering_words, select_lections_verbs,
                             )

app_name = 'exercises'
urlpatterns =[

    path('', exercises_page, name='exercises_page'),
    path('lections_ordering_words/', select_lections_ordering_words, name='select_lections_ordering_words'),
    path('lections_verbs/', select_lections_verbs, name='select_lections_verbs'),
    # path('drf/exercises/ordering_words/', OrderingWords.as_view(), name='ordering_words_drf'),
    path('ordering_words/', OrderingWords.as_view(), name='ordering_words'),
    path('exercises_verbs/', VerbExercises.as_view(), name='exercises_verbs'),
    path('save_progress/', save_progress, name='save_progress'),
    path("exercises/verbs/results/repeat/", verb_results_repeat, name="verb_results_repeat"),
    path("exercises/verbs/results/stop/", verb_results_stop, name="verb_results_stop"),

]