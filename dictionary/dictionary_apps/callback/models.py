from django.db import models
from dictionary.dictionary_apps.users.models import BaseUser

class SiteMessage(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='sent_message',
                             help_text='Кто отправил сообщение')
    recipient = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='received_message',
                             help_text='Кому адресовано сообщение', null=True, blank=True,)
    text = models.TextField()
    is_answered = models.BooleanField(default=False)
    answer_text = models.TextField(blank=True, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(blank=True, null=True)
    telegram_id = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return f"{self.user.email} | {self.created_at}"
