import json
import os
import requests


from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin


from dictionary.config.django.base import BOT_TOKEN, CHAT_ID
from dictionary.dictionary_apps.users.models import BaseUser
from dictionary.dictionary_apps.users.repository import UsersRepository
from dictionary.dictionary_apps.users.services import UsersService



def send_message(chat_id: int, text: str):
    print('SEND')
    if not BOT_TOKEN:
        print("Ошибка: BOT_TOKEN пустой")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",  # можно убрать, если не нужен HTML
    }
    try:
        response = requests.post(url, json=payload)
        print("Ответ Telegram API:", response.status_code, response.text)
    except Exception as e:
        print("Ошибка при отправке сообщения:", e)
class CallBackTelegram(LoginRequiredMixin, APIView):

    def post(self, request):
        print('FASFAFAFAFWAAWGFWEF')
#if request.method == 'POST':
        contact = request.data.get('contact')
        message = request.data.get('message')

        text = f"📩 Новое сообщение с сайта\n\n👤 Контакт: {contact}\n💬 Сообщение: {message}"

        if BOT_TOKEN and CHAT_ID:
            url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
            requests.post(url, data = {'chat_id': CHAT_ID, 'text': text})
            return redirect('api:main_page')
        return Response({"status": "error", "msg": "BOT_TOKEN или CHAT_ID не настроены"}, status=500)
  #      return Response({"status": "error", "msg": "Метод не поддерживается"}, status=405)


def ask_email(chat_id):
    print('ASK EMAIL')
    # if not BOT_TOKEN:
    #     print("Ошибка: BOT_TOKEN пустой")
    #     return
    if not chat_id:
        print("Ошибка: chat_id пустой")
        return
    # url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    text = "Привет! Чтобы связаться с вами, пожалуйста, пришлите ваш email."
    send_message(chat_id, text)
    # payload = {
    #     'chat_id': chat_id,
    #     'text': text
    # }
    # try:
    #     response = requests.post(url, json=payload)
    #     print("Telegram API response:", response.status_code, response.text)
    # except Exception as e:
    #     print("Ошибка при отправке ask_email:", e)
    #requests.post(url, json=payload)



@method_decorator(csrf_exempt, name='dispatch')
class CallBackWebhookTelegram(APIView):
    def post(self, request):
        print('WEBHOOK')
        try:
            data = json.loads(request.body)
        except Exception as e:
            print("JSON Error:", e)
            return Response({'ok': False, 'error': 'Invalid JSON'}, status=400)

        message = data.get('message')
        if not message:
            return Response({'ok': True})

        chat = message.get('chat', {})
        chat_id = chat.get('id')
        first_name = chat.get("first_name", "")
        username = chat.get("username", "")

        user = None
        try:
            user = UsersService(UsersRepository()).get_user_by_chat_id(chat_id)
            print(f"Найден пользователь по chat_id: {user.email}")
        except Exception as e:
            print(f"Ошибка при поиске пользователя: {e}")
        if not user:
            print(f"Пользователь с chat_id={chat_id} не найден, спрашиваем email")
            text = message.get('text')
            if text and '@' in text and "." in text:
                try:
                    UsersService(UsersRepository()).set_chat_id_by_email(chat_id, text)
                    send_message(chat_id, "Спасибо! Теперь я смогу писать вам сюда 🙌")
                except Exception as e:
                    print(f"Ошибка при вызове ask_email: {e}")
                    send_message(chat_id, "Произошла ошибка при сохранении emeil" )
            else:
                ask_email(chat_id)
                # Если пользователь найден — логируем
        else:
            print(f"Найден пользователь по chat_id: {user.email}")
        return Response({'ok': True})









