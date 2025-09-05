import django_filters

from dictionary.dictionary_apps.words.models import Word, Noun, Verb, Article, Lection


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