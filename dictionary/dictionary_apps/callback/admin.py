from django.contrib import admin

from .models import SiteMessage, Qwiz
@admin.register(SiteMessage)
class SiteMessageAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'recipient', 'text', 'is_answered', 'answer_text',
                    'created_at', 'answered_at', 'telegram_id')


@admin.register(Qwiz)
class QwizAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'recipient', 'question', 'options', 'answer_text',
                    'created_at', 'poll_id')