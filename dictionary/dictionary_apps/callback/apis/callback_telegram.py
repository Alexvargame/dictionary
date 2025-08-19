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
class CallBackTelegram(LoginRequiredMixin, APIView):

    def post(self, request):
        print('FASFAFAFAFWAAWGFWEF')
        if request.method == 'POST':
            contact = request.POST.get('contact')
            message = request.POST.get('message')

            text = f"📩 Новое сообщение с сайта\n\n👤 Контакт: {contact}\n💬 Сообщение: {message}"

            if BOT_TOKEN and CHAT_ID:
                url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
                requests.post(url, data = {'chat_id': CHAT_ID, 'text': text})
                return redirect('api:main_page')
            return Response({"status": "error", "msg": "BOT_TOKEN или CHAT_ID не настроены"}, status=500)
        return Response({"status": "error", "msg": "Метод не поддерживается"}, status=405)





@method_decorator(csrf_exempt, name='dispatch')
class CallBackWebhookTelegram(APIView):
        def post(self, request):
            print('WEBHOOK')
            if request.method != 'POST':
                return Response({'ok': False}, status=405)
            data = json.loads(request.body)
            message = data.get('message')
            if not message:
                return Response({'ok': True})
            chat = message.get('chat', {})
            chat_id = chat.get('id')
            first_name = chat.get("first_name", "")
            username = chat.get("username", "")
            try:
                user = UsersService(UsersRepository()).get_user_by_chat_id(chat_id)
                # Пользователь найден — можно продолжать переписку
                print(f"Найден пользователь по chat_id: {user.email}")
            except:
                pass


















