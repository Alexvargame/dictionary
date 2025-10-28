from typing import Optional

from django.db.models.query import QuerySet

from dictionary.dictionary_apps.common.utils import (get_object)
from dictionary.dictionary_apps.callback.filters import MessageFilter, QwizFilter
from dictionary.dictionary_apps.callback.models import SiteMessage, Qwiz




def message_list(*, filters=None):
    filters = filters or {}
    qs = SiteMessage.objects.all()
    return MessageFilter(filters, qs).qs

def message_get(message_id):
    message = get_object(SiteMessage, id=message_id)
    return message



def qwiz_list(*, filters=None):
    filters = filters or {}
    qs = Qwiz.objects.all()
    return QwizFilter(filters, qs).qs

def qwiz_get(qwiz_id):
    qwiz = get_object(Qwiz, id=qwiz_id)
    return qwiz
































