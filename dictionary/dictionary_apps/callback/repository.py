from dictionary.dictionary_apps.callback.models import SiteMessage, Qwiz


from django.db import transaction

from dictionary.dictionary_apps.callback.selectors import message_list, qwiz_list
from dictionary.dictionary_apps.dtos.callback.response_dto import MessagerDTO, QwizDTO
from dictionary.dictionary_apps.dtos.callback.request_dto import CreateMessageDTO, CreateQwizDTO
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

    def get_message_for_id(self, message_id):
        print('GET_MESS_FOR_TEL_ID', message_id)
        message = self.model.objects.get(id=message_id)
        return message

class QwizRepository:
    model = Qwiz
    dto = QwizDTO

    @transaction.atomic
    def create_object(self, dto):
        qwiz = self.model.objects.create(
            user=dto.user,
            question=dto.question,
            poll_id=dto.poll_id,
            recipient=dto.recipient,
            options=dto.options,
            correct_answer=dto.correct_answer

            # is_answered=dto.is_answered,
            # answer_text=dto.answer_text,
            # created_at=dto.created_at,
            # answered_at=dto.answered_at,
        )
        return qwiz

    def detail_object(self, obj):
        dto = self.dto (
            id=obj.id,
            user=obj.user,
            question=obj.question,
            options=dto.options,
            answer_text=obj.answer_text,
            created_at=obj.created_at,
            poll_id=obj.poll_id,
            recipient=obj.recipient,
            correct_answer=obj.correct_answer
        )
        return dto

    def list_objects(self, filters=None):
        lst_dto = []
        print('FILR', filters)
        for obj in qwiz_list(filters=filters):
            tmp_dto = self.dto(
                id=obj.id,
                user=obj.user,
                question=obj.question,
                options=dto.options,
                answer_text=obj.answer_text,
                created_at=obj.created_at,
                poll_id=obj.poll_id,
                recipient=obj.recipient,
                correct_answer=obj.correct_answer
            )
            lst_dto.append(tmp_dto)
        return lst_dto
    @transaction.atomic
    def update_object(self, dto):
        print('UPDATE_QWIZ_DTO', dto, dto.id)
        mqwiz = self.model.objects.get(id=dto.id)
        for key, value in dto.__dict__.items():
           qwiz.__dict__[key] = value
        # user, has_updated = model_update(instance=user, fields=non_side_effect_fields, data=data)
        qwiz.save()

    @transaction.atomic
    def delete_object(self, qwiz_id):
        qwiz = self.model.objects.get(id=qwiz_id)
        qwiz.delete()

    def get_qwiz_for_poll_id(self, qwiz_poll_id):
        print('GET_qwiz_FOR_TEL_ID', qwiz_poll_id)
        qwiz = self.model.objects.filter(poll_id=qwiz_poll_id).first()
        return qwiz

    def get_qwiz_for_id(self, qwiz_id):
        print('GET_QWIz_FOR_TEL_ID', qwiz_id)
        qwiz = self.model.objects.get(id=qwiz_id)
        return qwiz