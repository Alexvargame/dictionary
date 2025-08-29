from typing import List, Optional

from django.db import transaction

class MessageService:

    def __init__(self, repository):
        self.repository = repository

    def create_object(self, dto):
        return self.repository.create_object(dto)


    def detail_object(self, obj):
        return self.repository.detail_object(obj)

    def list_objects(self, filters=None):
        return self.repository.list_objects(filters)

    def update_object(self, dto):
        return self.repository.update_object(dto)

    def delete_object(self, obj_id):
        return self.repository.delete_object(obj_id)

    def get_message_for_id(self, message_id):
        return self.repository.get_message_for_id(message_id)

    def get_message_for_telegram_id(self, message_telegram_id):
        message = self.repository.get_message_for_telegram_id(message_telegram_id)
        if not message:
            print(f"[!] Сообщение с telegram_id={message_telegram_id} не найдено")
            return None
        return message