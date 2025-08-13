from django.urls import path

from .apis.callback_telegram import CallBackTelegram

app_name = 'callback'

urlpatterns =[
    path('telegram', CallBackTelegram.as_view(), name='send_telegram_message')
]