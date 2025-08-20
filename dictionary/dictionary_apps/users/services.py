from typing import List, Optional

from django.db import transaction

from dictionary.dictionary_apps.users.models import BaseUser


@transaction.atomic
def user_create(*, email, username, name=None, surname=None, phone=None, is_active=True, is_admin=False, user_role=1, password=None):
    print(email, username, name, surname, phone, is_active, is_admin, user_role)
    user = BaseUser.objects.create_user(email=email, username=username, name=name, surname=surname,
                                        phone=phone, is_active=is_active, user_role=user_role, password=password)
    return user

class UsersService:

    def __init__(self, repository):
        self.repository = repository

    def create_object(self, dto):
        return self.repository.create_object(dto)


    def detail_object(self, obj):
        return self.repository.detail_object(obj)

    def list_objects(self):
        return self.repository.list_objects()

    def update_object(self, dto):
        return self.repository.update_object(dto)

    def get_user_by_email(self, email):
        return self.repository.get_user_by_email(email)

    def get_user_by_chat_id(self, chat_id):
        print('CHAT_ID', chat_id)
        return self.repository.get_user_by_chat_id(chat_id)

    def set_chat_id_by_email(self, chat_id, email):
        self.repository.set_chat_id_by_email(chat_id, email)