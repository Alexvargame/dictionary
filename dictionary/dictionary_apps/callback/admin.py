from django.contrib import admin

from .models import SiteMessage
@admin.register(SiteMessage)
class SiteMessageAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'recipient', 'text', 'is_answered', 'answer_text',
                    'created_at', 'answered_at', 'telegram_id')


