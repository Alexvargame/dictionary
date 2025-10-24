from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from rest_framework.views import APIView
import datetime

from dictionary.config.django.base import CHAT_ID
from dictionary.dictionary_apps.callback.models import SiteMessage
from dictionary.dictionary_apps.callback.filters import MessageFilter
from dictionary.dictionary_apps.callback.repository import MessageRepository
from dictionary.dictionary_apps.callback.services import MessageService
from dictionary.dictionary_apps.dtos.callback.response_dto import MessagerDTO
from dictionary.dictionary_apps.callback.apis.callback_telegram import send_message

@method_decorator(staff_member_required, name='dispatch')
class MessageListApiFront(FilterView):
    model = SiteMessage
    template_name = 'callback/messages_list.html'
    filterset_class = MessageFilter
    context_object_name = 'messages'
    paginate_by = 20

def unanswered_messages(request):
    # Берем все сообщения, у которых нет reply
    messages = SiteMessage.objects.filter(
        is_answered = False
    ).order_by("-created_at")

    return render(request, "callback/unanswered_messages.html", {"messages": messages})

@method_decorator(staff_member_required, name='dispatch')
class ReplyMessageApi(APIView):

    def post(self, request, message_id):
        message = MessageService(MessageRepository()).get_message_for_id(message_id)

        reply_text = request.POST.get('reply')
        print('ans_message_reply_text', message, message.text, reply_text)
        if not reply_text:
            return redirect('api:callback:messages_list_sort')
        if reply_text:
            dto = MessagerDTO(
                id=message.id,
                user=message.user,
                text=message.text,
                is_answered=True,
                answer_text=reply_text,
                created_at=message.created_at,
                answered_at=datetime.datetime.now(),
                telegram_id=message.telegram_id,
                recipient=message.recipient,
            )
            MessageService(MessageRepository()).update_object(dto)
        print('Aдресат', message.recipient, message.recipient.chat_id)
        if message.recipient.chat_id:
            formatted_reply = (
                f"Email: {dto.recipient.email}\n"
                f"Username: {dto.recipient.telegram_username}\n"
                f"ChatID: {dto.recipient.chat_id}\n"
                f"Telegram_id: {dto.telegram_id}\n"
                f"Text: {dto.answer_text}"
            )
            print('Answr', formatted_reply)
            send_message(dto.user.chat_id, formatted_reply)
            send_message(int(CHAT_ID), f"✅ Ответ отправлен пользователю {dto.recipient.chat_id}")

        return redirect('api:callback:messages_list_sort')
