from django.urls import path
#
# from .apis import (NounCreateApi, NounDetailApi, NounListApi,
#                         NounDeleteApi, NounUpdateApi,
#                   )
from .apis.odering_words import OrderingWords, save_progress
from .apis.verbs_exercises import VerbExercises, verb_results_stop, verb_results_repeat
from .apis.article_words import ArticleNouns, article_results_stop, article_results_repeat
from .apis.digits import Digits, digits_results_stop, digits_results_repeat
from .apis.exercises import (exercises_page, select_lections_ordering_words, select_lections_verbs,
                            select_lections_article_words,
                             )

app_name = 'exercises'
urlpatterns =[

    path('', exercises_page, name='exercises_page'),
    path('lections_ordering_words/', select_lections_ordering_words, name='select_lections_ordering_words'),
    path('lections_article_words/', select_lections_article_words, name='select_lections_article_words'),
    path('article_words/', ArticleNouns.as_view(), name='article_words'),
    path('lections_verbs/', select_lections_verbs, name='select_lections_verbs'),
    path('digits/', Digits.as_view(), name='digits'),
    # path('drf/exercises/ordering_words/', OrderingWords.as_view(), name='ordering_words_drf'),
    path('ordering_words/', OrderingWords.as_view(), name='ordering_words'),
    path('exercises_verbs/', VerbExercises.as_view(), name='exercises_verbs'),
    path('save_progress/', save_progress, name='save_progress'),
    path("exercises/verbs/results/repeat/", verb_results_repeat, name="verb_results_repeat"),
    path("exercises/verbs/results/stop/", verb_results_stop, name="verb_results_stop"),
    path("exercises/article_words/results/repeat/", article_results_repeat, name="article_results_repeat"),
    path("exercises/article_words/results/stop/", article_results_stop, name="article_results_stop"),
    path("exercises/digits/results/repeat/", digits_results_repeat, name="digits_results_repeat"),
    path("exercises/digits/results/stop/", digits_results_stop, name="digits_results_stop"),

]