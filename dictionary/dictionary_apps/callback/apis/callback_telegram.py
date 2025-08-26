import json
import os
import re

import requests
import datetime

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

def handle_command_user_message(chat_id, text):
    # Пример: "/message_user @alex Привет, тест!"
    # if text.startswith("/message_user"):
    print('TO USER', chat_id, text)
    parts = text.split(" ", 2)  # ['/message_user', '@alex', 'Привет, тест!']
    if len(parts) < 3:
        send_message(chat_id, "❌ Использование: /message_user <username|chat_id> <текст>")
        return

    target, msg_text = parts[1], parts[2]
    print('PSTSR', target, msg_text)
    # Если указали username
    if target.startswith("@"):
        username = target[1:]
        try:
            abonent_user = UsersService(UsersRepository()).get_user_by_telegraam_username(username)
            if abonent_user.chat_id:
                print(abonent_user)
                return abonent_user, msg_text
                # send_message(user.telegram_chat_id, msg_text)
                # send_message(chat_id, f"✅ Сообщение отправлено {target}")
            else:
                send_message(chat_id, f"⚠️ У пользователя {target} нет chat_id")
        except User.DoesNotExist:
            send_message(chat_id, f"❌ Пользователь {target} не найден")

    # Если указали просто chat_id
    elif target.isdigit():
        try:
            abonent_user = UsersService(UsersRepository()).get_user_by_chat_id(chat_id)
            return abonent_user, msg_text
        except:
            send_message(chat_id, f"Неверный chat_id абонента")

        # send_message(int(target), msg_text)
        # send_message(chat_id, f"✅ Сообщение отправлено chat_id {target}")
    else:
        send_message(chat_id, "❌ Неверный формат команды")
        return None, None

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
        message_telegram_id = messagetext.get('id')
        user = UsersService(UsersRepository()).get_user_by_email(contact)
        dto = CreateMessageDTO(
            user = user,
            text = messagetext,
            telegram_id = message_telegram_id
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
        message_telegram_id = message.get('message_id')
        print('MESSAGE', message)
        if not message:
            return Response({'ok': True})
        chat = message.get('chat', {})
        chat_id = chat.get('id')
        first_name = chat.get("first_name", "")
        username = chat.get("username", "")
        text = (message.get('text') or '').strip()
        print('TEXT', text)
        reply_to = message.get('reply_to_message')
        print('TO_REPLY', reply_to, type(reply_to))
        if reply_to and isinstance(reply_to, dict):
            if chat_id == int(CHAT_ID):
                original_text = reply_to.get('text', '')
                print('ORIGINAL', original_text)
                message_telegram_id = int(original_text.split('Telegram_id: ')[1].split('\n')[0])
                print('MESS__TEL__ID',message_telegram_id)
                message_for_reply = MessageService(MessageRepository()).get_message_for_telegram_id(message_telegram_id)
                print('MESSAGE_FOR_RAPLY_BEFORE', message_for_reply)
                if not message_for_reply.is_answered:
                    dto = MessagerDTO(
                        id=message_for_reply.id,
                        user=message_for_reply.user,
                        text=message_for_reply.text,
                        is_answered=True,
                        answer_text=text,
                        created_at=message_for_reply.created_at,
                        answered_at=datetime.datetime.now(),
                        telegram_id=message_for_reply.telegram_id,
                    )
                    MessageService(MessageRepository()).update_object(dto)
                    print('MESSAGE_FOR_RAPLY_AFTER', message_for_reply)
                    if text:
                        send_message(int(dto.user.chat_id), text)
                    reply_text = text
                    if reply_text:
                        formatted_reply = (
                            f"Email: {dto.user.email}\n"
                            f"Username: {dto.user.telegram_username}\n"
                            f"ChatID: {dto.user.chat_id}\n"
                            # f"Telegram_id: {message_telegram_id}\n"
                            f"Text: {dto.reply_text}"
                        )
                        print('TARGET', dto.user.chat_id)
                        send_message(dto.user.chat_id, formatted_reply)
                        print('FORMST', formatted_reply )
                        send_message(int(CHAT_ID), f"✅ Ответ отправлен пользователю {dto.user.chat_id}")
                        return Response({'ok': True})

                    else:
                        print('DIDNT fIND CHAT ID')
                else:
                    print('УЖЕ ОТВЕЧЕНО!!!!')
                    Response({'ok': True})
        else:
            print('NOT REPLY')
        user = None
        try:
            user = UsersService(UsersRepository()).get_user_by_chat_id(chat_id)
            if user.telegram_username == None:
                UsersService(UsersRepository()).set_telegram_username(chat_id, chat_id.get('username'))
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
                print('sTART')
                send_message(user.chat_id,
                             f"Привет, {first_name or user.email}! Вы уже связаны с ботом 🙌\nНапишите сюда сообщение — я передам его оператору.")
                return Response({'ok': True})
            if text.startswith("/message_user"):
                abonent_user, message_text = handle_command_user_message(int(CHAT_ID), text)
                print(abonent_user, message_text)
                if abonent_user_user and message_text:
                    dto = CreateMessageDTO(
                        user=user,
                        text=message_text,
                        telegram_id=message_telegram_id,
                    )
                    print('DTO', dto)
                    message_user = MessageService(MessageRepository()).create_object(dto)
                    print('MESS_USE', message_user)
                    message_note = (
                        f"📩 Сообщение от пользователя\n"
                        f"Email: {message_user.user.email or '—'}\n"
                        f"Username: @{username or '—'}\n"
                        f"ChatID: {message_user.user.chat_id}\n"
                        f"Telegram_id: {message_user.telegram_id}\n"
                        f"Текст: {message_user.text}"
                        f"Пользователю {abonent_user}\n"
                        f"ChatID: {abonent_user.chat_id}"
                    )
                    send_message(abonent_user.chat_id, message_note)
                    return Response({'ok': True})
                else:
                    return

            # 2) Любое другое сообщение — перекидываем админу и подтверждаем юзеру
            if text:
                print('REPLYSTART')
                dto = CreateMessageDTO(
                    user = user,
                    text = text,
                    telegram_id=message_telegram_id,
                )
                print('DTO', dto)
                message_user = MessageService(MessageRepository()).create_object(dto)
                print('MESS_USE', message_user)
                admin_note = (
                    f"📩 Сообщение от пользователя\n"
                    f"Email: {message_user.user.email or '—'}\n"
                    f"Username: @{username or '—'}\n"
                    f"ChatID: {message_user.user.chat_id}\n"
                    f"Telegram_id: {message_user.telegram_id}\n"
                    f"Текст: {message_user.text}"
                )
                print('ADMINNITE', admin_note)
                send_message(int(CHAT_ID), admin_note)
                send_message(message_user.user.chat_id, "Принял! Передал сообщение оператору. Ответ придёт сюда.")
                return Response({'ok': True})

            # Если пришёл не текст (стикер/фото и т.п.)
            send_message(message.user.chat_id, "Пока принимаю только текстовые сообщения 🙂")
            # return Response({'ok': True})
        return Response({'ok': True})







