from django.contrib import admin
from .models import (Book, Lection, Article, WordType, Word,
                     Noun, Verb, Adjective, Numeral, Pronoun,
                     NounDeclensionsForm, OtherWords)


@admin.register(WordType)
class WordTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')


@admin.register(Lection)
class LectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'name', 'description')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'forms')

#
@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('id', 'word_type',  'lection')

@admin.register(Noun)
class NounAdmin(admin.ModelAdmin):
    list_display = ('id', 'word', 'word_translate',
                    'word_plural', 'word_translate_plural',
                    'plural_sign', 'article'
                    )
@admin.register(Verb)
class VerbAdmin(admin.ModelAdmin):
    list_display = ('id', 'word', 'word_translate',
                    'ich_form', 'du_form', 'er_sie_es_form',
                    'wir_form', 'ihr_form', 'Sie_sie_form',
                    'past_perfect_form', 'past_prateritum_ich_form',
                      'past_prateritum_du_form', 'past_prateritum_er_sie_es_form',
                      'past_prateritum_wir_form', 'past_prateritum_ihr_form',
                      'past_prateritum_Sie_sie_form', 'lection', 'word_type',
                    'regal'
                    )


@admin.register(Adjective)
class AdjectiveAdmin(admin.ModelAdmin):
    list_display = ('id', 'word', 'word_translate', 'lection',
                    'komparativ', 'superlativ', 'declensions'
                    )

@admin.register(Numeral)
class NumeralAdmin(admin.ModelAdmin):
    list_display = ('id', 'word', 'word_translate', 'lection',
                    'ordinal', 'date_numeral',
                    )
@admin.register(Pronoun)
class PronounAdmin(admin.ModelAdmin):
    list_display = ('id', 'word', 'word_translate', 'lection',
                    'akkusativ', 'akkusativ_translate', 'dativ',
                    'dativ_translate', 'prossessive',
                    'prossessive_translate','reflexive',)

@admin.register(NounDeclensionsForm)
class NounDeclensionsFormAdmin(admin.ModelAdmin):
    list_display = ('id', 'noun','nominativ',
    'genitiv', 'dativ', 'akkusativ',
    'plural_nominativ', 'plural_genitiv',
    'plural_dativ', 'plural_akkusativ')

@admin.register(OtherWords)
class OtherWordsAdmin(admin.ModelAdmin):
    list_display = ('id', 'word', 'word_translate')