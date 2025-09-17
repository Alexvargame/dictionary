import django_filters

from dictionary.dictionary_apps.words.models import (Word, Noun, Verb, Article,
                                                     Lection, Numeral, Adjective, Pronoun)


class WordFilter(django_filters.FilterSet):
    id = django_filters.BaseInFilter(field_name='id', lookup_expr='in')
    class Meta:
        model = Word
        fields = ("id", "lection")

class NounFilter(django_filters.FilterSet):
    id = django_filters.BaseInFilter(field_name='id', lookup_expr='in')
    class Meta:
        model = Noun
        fields = ("id", "article")

class VerbFilter(django_filters.FilterSet):
    id = django_filters.BaseInFilter(field_name='id', lookup_expr='in')
    class Meta:
        model = Verb
        fields = ("id", )

class NumeralFilter(django_filters.FilterSet):
    id = django_filters.BaseInFilter(field_name='id', lookup_expr='in')
    class Meta:
        model = Numeral
        fields = ("id", )

class AdjectiveFilter(django_filters.FilterSet):
    id = django_filters.BaseInFilter(field_name='id', lookup_expr='in')
    class Meta:
        model = Adjective
        fields = ("id", )

class PronounFilter(django_filters.FilterSet):
    id = django_filters.BaseInFilter(field_name='id', lookup_expr='in')
    class Meta:
        model = Pronoun
        fields = ("id", )
class ArticleFilter(django_filters.FilterSet):
    id = django_filters.BaseInFilter(field_name='id', lookup_expr='in')
    class Meta:
        model = Article
        fields = ("id", )

class LectionFilter(django_filters.FilterSet):
    id = django_filters.BaseInFilter(field_name='id', lookup_expr='in')
    class Meta:
        model = Lection
        fields = ('id', 'book')