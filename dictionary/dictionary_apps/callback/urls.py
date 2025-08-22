from django.urls import path

from .apis.callback_telegram import CallBackTelegram, CallBackWebhookTelegram
from .apis.crud_message import (MessageCreateApi, MessageDetailApi,MessageListApi,
                                MessageUpdateApi, MessageDeleteApi)

app_name = 'callback'

urlpatterns =[
    path('send_telegram_message/', CallBackTelegram.as_view(), name='send_telegram_message'),
    path('webhook/', CallBackWebhookTelegram.as_view(), name='telegram_webhook'),

    path('message/', MessageListApi.as_view(), name='messages_list'),
    path('message/create/', MessageCreateApi.as_view(), name='message_create'),
    path('message/<int:message_id>/', MessageDetailApi.as_view(), name='message_detail'),
    path('message/<int:message_id>/update/', MessageUpdateApi.as_view(), name='message_update'),
    path('message/<int:message_id>/delete/', MessageDeleteApi.as_view(), name='message_delete'),
]