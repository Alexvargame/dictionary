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
from dictionary.dictionary_apps.callback.models import SiteMessage
from dictionary.dictionary_apps.dtos.callback.response_dto import MessagerDTO
from dictionary.dictionary_apps.dtos.callback.request_dto import CreateMessageDTO
from dictionary.dictionary_apps.callback.repository import MessageRepository
from dictionary.dictionary_apps.callback.services import MessageService



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
        contact = request.data.get('contact')
        messagetext = request.data.get('message')
        user = UsersService(UsersRepository()).get_user_by_email(contact)
        dto = CreateMessageDTO(
            user = user,
            text = messagetext,
        )
        message = MessageService(MessageRepository()).create_object(dto)
        text = f"📩 Новое сообщение с сайта\n\n👤 Контакт: {message.user}\n💬 Сообщение: {message.text}"
        if BOT_TOKEN and CHAT_ID:
            url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
            requests.post(url, data = {'chat_id': user.chat_id, 'text': text})
            return redirect('api:main_page')
        return Response({"status": "error", "msg": "BOT_TOKEN или CHAT_ID не настроены"}, status=500)

def ask_email(chat_id):
    print('ASK EMAIL')
    if not chat_id:
        print("Ошибка: chat_id пустой")
        return
    text = "Привет! Чтобы связаться с вами, пожалуйста, пришлите ваш email."
    send_message(chat_id, text)




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
        print('MESSAGE', message)
        if not message:
            return Response({'ok': True})
        chat = message.get('chat', {})
        chat_id = chat.get('id')
        first_name = chat.get("first_name", "")
        username = chat.get("username", "")
        text = (message.get('text') or '').strip()
        print('TEXT', text)
        if chat_id == CHAT_ID:
            print('from admin')
            reply_to = message.get('reply_to_message')
            print('TO_REPLY', reply_to, type(reply_to))
            if reply_to and isinstance(reply_to, dict):
                original_text = reply_to.get('text', '')
                print('ORIGINAL', original_text)
            else:
                print('NOT REPY or is not a dict')
            if reply_to:
                print('TO_REPLY', reply_to)
                original_text = reply_to.get('text', '')
                print('ORIGINAL', original_text)
                match = re.search(r"ChatID:\s*(\d+)", original_text)
                if match:
                    print('Find CHATID', match.group(1))
                    target_chat_id = int(match.group(1))
                    if text:
                        send_message(target_chat_id, text)
                    reply_text = text
                    if reply_text:
                        email_match = re.search(r"Email:\s*(.+)", original_text)
                        username_match = re.search(r"Username:\s*(.+)", original_text)
                        email = email_match.group(1) if email_match else '—'
                        uname = username_match.group(1) if username_match else '—'

                        formatted_reply = (
                            f"Email: {email}\n"
                            f"Username: {uname}\n"
                            f"ChatID: {target_chat_id}\n"
                            f"Text: {reply_text}"
                        )
                        print('TARGET', target_chat_id)
                        send_message(target_chat_id, formatted_reply)
                        print('FORMST', formatted_reply )
                        send_message(int(CHAT_ID), f"✅ Ответ отправлен пользователю {target_chat_id}")
                        return Response({'ok': True})

                else:
                    print('DIDNT fIND CHAT ID')
            else:
                print('NOT REPLY')
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
            # 1) Повторный /start
            if text == '/start':
                send_message(user.chat_id,
                             f"Привет, {first_name or user.email}! Вы уже связаны с ботом 🙌\nНапишите сюда сообщение — я передам его оператору.")
                return Response({'ok': True})

            # 2) Любое другое сообщение — перекидываем админу и подтверждаем юзеру
            if text:
                dto = CreateMessageDTO(
                    user = user,
                    text = text,
                )
                message_user = MessageService(MessageRepository()).create_object(dto)
                print('NEWMESS', message_user)
                print('iuser', message_user.user)
                print('emal', message_user.user.email)

                admin_note = (
                    f"📩 Сообщение от пользователя\n"
                    f"Email: {message_user.user.email or '—'}\n"
                    f"Username: @{message_user.user.username or '—'}\n"
                    f"ChatID: {message_user.user.chat_id}\n\n"
                    f"Текст: {message_user.text}"
                )
                send_message(int(CHAT_ID), admin_note)
                send_message(message_user.user.chat_id, "Принял! Передал сообщение оператору. Ответ придёт сюда.")
                return Response({'ok': True})

            # Если пришёл не текст (стикер/фото и т.п.)
            send_message(message.user.chat_id, "Пока принимаю только текстовые сообщения 🙂")
            # return Response({'ok': True})
        return Response({'ok': True})







