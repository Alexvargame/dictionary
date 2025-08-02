from django.urls import path
#
# from .apis import (NounCreateApi, NounDetailApi, NounListApi,
#                         NounDeleteApi, NounUpdateApi,
#                   )
from .apis.odering_words import OrderingWords, save_progress
from .apis.exercises import exercises_page

app_name = 'exercises'
urlpatterns =[

    path('', exercises_page, name='exercises_page'),
    # path('drf/exercises/ordering_words/', OrderingWords.as_view(), name='ordering_words_drf'),
    path('ordering_words/', OrderingWords.as_view(), name='ordering_words'),
    path('save_progress/', save_progress, name='save_progress'),

]