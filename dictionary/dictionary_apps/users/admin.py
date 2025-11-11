from django.contrib import admin
from django.core.exceptions import ValidationError

from dictionary.dictionary_apps.users.models import BaseUser
from dictionary.dictionary_apps.users.services import user_create


@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'name', 'surname', 'email', 'is_admin', 'registration_date',
                    'phone', 'last_login_date', 'is_active', 'user_role', 'score', 'lifes', 'chat_id',
                    'telegram_username', 'user_bot_pass', 'user_bot_id', 'last_life_update')
    search_fields = ('email', 'user_role')
    fieldsets = (
        (None, {'fields': ('email', 'username','name', 'surname', 'user_role')}),
        ('Booleans', {'fields': ('is_active','is_admin')}),
        ('Timestamps', {'fields': ('registration_date', 'last_login_date')})
    )

    readonly_fields = ('registration_date', 'last_login_date')

    def save_model(self, request, obj, form, change):
        if change:
            return super().save_model(request, obj, form, change)
        try:
            print('FORM_CLEAN_DATA', form.cleaned_data)
            user_create(**form.cleaned_data)
        except ValidationError as exc:
            self.message_user(request, str(), message.ERROR)
