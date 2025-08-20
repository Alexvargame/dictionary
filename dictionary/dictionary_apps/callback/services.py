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
