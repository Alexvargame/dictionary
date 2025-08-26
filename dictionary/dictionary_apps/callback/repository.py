from dictionary.dictionary_apps.callback.models import SiteMessage


from django.db import transaction

from dictionary.dictionary_apps.callback.selectors import message_list
from dictionary.dictionary_apps.dtos.callback.response_dto import MessagerDTO
from dictionary.dictionary_apps.dtos.callback.request_dto import CreateMessageDTO
from dictionary.dictionary_apps.common.services import model_update






class MessageRepository:
    model = SiteMessage
    dto = MessagerDTO

    @transaction.atomic
    def create_object(self, dto):
        message = self.model.objects.create(
            user=dto.user,
            text=dto.text,
            telegram_id=dto.telegram_id,
            recipient=dto.recipient,
            # is_answered=dto.is_answered,
            # answer_text=dto.answer_text,
            # created_at=dto.created_at,
            # answered_at=dto.answered_at,
        )
        return message

    def detail_object(self, obj):
        dto = self.dto (
            id=obj.id,
            user=obj.user,
            text=obj.text,
            is_answered=obj.is_answered,
            answer_text=obj.answer_text,
            created_at=obj.created_at,
            answered_at=obj.answered_at,
            telegram_id=obj.telegram_id,
            recipient=obj.recipient,
        )
        return dto

    def list_objects(self, filters=None):
        lst_dto = []
        print('FILR', filters)
        for obj in message_list(filters=filters):
            tmp_dto = self.dto(
                id=obj.id,
                user=obj.user,
                text=obj.text,
                is_answered=obj.is_answered,
                answer_text=obj.answer_text,
                created_at=obj.created_at,
                answered_at=obj.answered_at,
                telegram_id=obj.telegram_id,
                recipient=obj.recipient,
            )
            lst_dto.append(tmp_dto)
        return lst_dto
    @transaction.atomic
    def update_object(self, dto):
        print('UPDATE_MESS_DTO', dto, dto.id)
        message = self.model.objects.get(id=dto.id)
        for key, value in dto.__dict__.items():
           message.__dict__[key] = value
        # user, has_updated = model_update(instance=user, fields=non_side_effect_fields, data=data)

        message.save()

    @transaction.atomic
    def delete_object(self, message_id):
        message = self.model.objects.get(id=message_id)
        message.delete()

    def get_message_for_telegram_id(self, message_telegram_id):
        print('GET_MESS_FOR_TEL_ID', message_telegram_id)
        message = self.model.objects.filter(telegram_id=message_telegram_id).first()
        return message