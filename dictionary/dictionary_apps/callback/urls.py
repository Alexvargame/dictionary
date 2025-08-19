from django.urls import path

from .apis.callback_telegram import CallBackTelegram, CallBackWebhookTelegram

app_name = 'callback'

urlpatterns =[
    path('send_telegram_message/', CallBackTelegram.as_view(), name='send_telegram_message'),
    path('webhook/', CallBackWebhookTelegram.as_view(), name='telegram_webhook'),
]