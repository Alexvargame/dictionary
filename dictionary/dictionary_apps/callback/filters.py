import django_filters
from django import forms
from dictionary.dictionary_apps.callback.models import SiteMessage


class MessageFilter(django_filters.FilterSet):
    id = django_filters.BaseInFilter(
        field_name='id',
        lookup_expr='in',
        widget=forms.TextInput#(attrs={'class': 'border rounded p-2 w-full'})
    )
    user = django_filters.CharFilter(
        field_name='user__email',
        lookup_expr='icontains',
        label='User email',
        widget=forms.TextInput,
    )
    is_answered = django_filters.ChoiceFilter(
        field_name='is_answered',
        choices=(
            ('', 'Все'),
            ('True', 'Отвеченные'),
            ('False', 'Неотвеченные'),
        ),
        widget=forms.Select,
        label='Статус',

    )

    dering = django_filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('user__email', 'user'),
        ),
        field_labels={
            'created_at': 'Дата',
            'user__email': 'Пользователь',
        },
        widget=forms.Select

    )
    class Meta:
        model = SiteMessage
        fields = ("id", "user", 'is_answered')
