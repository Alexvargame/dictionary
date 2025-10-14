import django_filters

from dictionary.dictionary_apps.users.models import BaseUser, UserRole


class BaseUserFilter(django_filters.FilterSet):
    class Meta:
        model = BaseUser
        fields = ("id", "email", "is_admin", "user_role")

class UserRoleFilter(django_filters.FilterSet):
    class Meta:
        model = UserRole
        fields = ("id", "name")