import django_filters

from dictionary.dictionary_apps.callback.models import SiteMessage


class MessageFilter(django_filters.FilterSet):
    id = django_filters.BaseInFilter(field_name='id', lookup_expr='in')
    class Meta:
        model = SiteMessage
        fields = ("id", "user", 'is_answered')
