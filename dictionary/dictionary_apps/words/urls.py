from django.urls import path

from .apis.neun import (NounCreateApi, NounDetailApi, NounListApi,
                        NounDeleteApi, NounUpdateApi,
                  )
from .apis.verb import (VerbDeleteApi, VerbDetailApi, VerbListApi,
                        VerbUpdateApi, VerbCreateApi)
app_name = 'words'
urlpatterns =[
    path('nouns/', NounListApi.as_view(), name='nouns_list'),
    path('nouns/create/', NounCreateApi.as_view(), name='noun_create'),
    path('nouns/<int:noun_id>/', NounDetailApi.as_view(), name='noun_detail'),
    path('nouns/<int:noun_id>/update/', NounUpdateApi.as_view(), name='noun_update'),
    path('nouns/<int:noun_id>/delete/', NounDeleteApi.as_view(), name='noun_delete'),

    path('verbs/', VerbListApi.as_view(), name='verbs_list'),
    path('verbs/create/', VerbCreateApi.as_view(), name='verb_create'),
    path('verbs/<int:verb_id>/', VerbDetailApi.as_view(), name='verb_detail'),
    path('verbs/<int:verb_id>/update/', VerbUpdateApi.as_view(), name='verb_update'),
    path('verbs/<int:verb_id>/delete/', VerbDeleteApi.as_view(), name='verb_delete'),


    # path('', WordListApi.as_view(), name='word_list'),
    # path('create/', WordCreateApi.as_view(), name='word_create'),
    # path('<int:word_id>/', WordDetailApi.as_view(), name='word_detail'),
    # path('<int:word_id>/update/', WordUpdateApi.as_view(), name='word_update'),
    #
    #path('exercises/', exercises_page, name='exercises_page'),
    # path('drf/exercises/ordering_words/', OrderingWords.as_view(), name='ordering_words_drf'),
    # path('exercises/ordering_words/', OrderingWords.as_view(), name='ordering_words'),
    # path('save_progress/', save_progress, name='save_progress'),

]