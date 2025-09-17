from django.urls import path

from .apis.neun import (NounCreateApi, NounDetailApi, NounListApi,
                        NounDeleteApi, NounUpdateApi,
                  )
from .apis.verb import (VerbDeleteApi, VerbDetailApi, VerbListApi,
                        VerbUpdateApi, VerbCreateApi)

from .apis.numeral import (NumeralCreateApi, NumeralListApi,
                           NumearalDetailApi, NumeralDeleteApi,
                           NumeralUpdateApi)
from .apis.adjectiv import (AdjectiveCreateApi, AdjectiveDetailApi,
                            AdjectiveDeleteApi, AdjectiveListApi,
                            AdjectiveUpdateApi)
from .apis.pronoun import (PronounListApi, PronounCreateApi,
                           PronounDeleteApi, PronounDetailApi,
                           PronounUpdateApi)
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

    path('numerals/', NumeralListApi.as_view(), name='numerals_list'),
    path('numerals/create/', NumeralCreateApi.as_view(), name='numeral_create'),
    path('numerals/<int:numeral_id>/', NumearalDetailApi.as_view(), name='numeral_detail'),
    path('numerals/<int:numeral_id>/update/', NumeralUpdateApi.as_view(), name='numeral_update'),
    path('numerals/<int:numeral_id>/delete/', NumeralDeleteApi.as_view(), name='numeral_delete'),

    path('adjectives/', AdjectiveListApi.as_view(), name='adjectives_list'),
    path('adjectives/create/', AdjectiveCreateApi.as_view(), name='adjective_create'),
    path('adjectives/<int:adjective_id>/', AdjectiveDetailApi.as_view(), name='adjective_detail'),
    path('adjectives/<int:adjective_id>/update/', AdjectiveUpdateApi.as_view(), name='adjective_update'),
    path('adjectives/<int:adjective_id>/delete/', AdjectiveDeleteApi.as_view(), name='adjective_delete'),

    path('pronouns/', PronounListApi.as_view(), name='pronouns_list'),
    path('pronouns/create/', PronounCreateApi.as_view(), name='pronoun_create'),
    path('pronouns/<int:pronoun_id>/', PronounDetailApi.as_view(), name='pronoun_detail'),
    path('pronouns/<int:pronoun_id>/update/', PronounUpdateApi.as_view(), name='pronoun_update'),
    path('pronouns/<int:pronoun_id>/delete/', PronounDeleteApi.as_view(), name='pronoun_delete'),
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