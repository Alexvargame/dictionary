from typing import Optional

from django.db.models.query import QuerySet

from dictionary.dictionary_apps.common.utils import get_object
from dictionary.dictionary_apps.users.filters import BaseUserFilter, UserRoleFilter
from dictionary.dictionary_apps.users.models import BaseUser, UserRole


def user_list(*, filters=None):
    filters = filters or {}
    qs = BaseUser.objects.all()
    return BaseUserFilter(filters, qs).qs

def user_get(user_id):
    user = get_object(BaseUser, id=user_id)
    print('gET-USR', user)
    return user

def user_role_list(*, filters=None):
    filters = filters or {}
    qs = UserRole.objects.all()
    return UserRoleFilter(filters, qs).qs

def user_role_get(user_role_id):
    user_role = get_object(UserRole, id=user_role_id)
    return user_role


























































