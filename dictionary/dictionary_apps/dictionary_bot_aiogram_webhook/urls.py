
from django.urls import include, path
from dictionary.dictionary_apps.dictionary_bot_aiogram_webhook.apis import telegram_bot_webhook
app_name = 'telegram_bot_aiogram_webhook'

urlpatterns =[
    path("", telegram_bot_webhook, name="telergam_bot_webhook"),

]