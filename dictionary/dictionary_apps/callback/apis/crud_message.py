from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import datetime

from dictionary.dictionary_apps.api.pagination import (
    LimitOffsetPagination,
    get_pagination_response,
)

from dictionary.dictionary_apps.callback.models import SiteMessage

from dictionary.dictionary_apps.callback.selectors import (message_list, message_get)
from dictionary.dictionary_apps.users.selectors import user_get

from dictionary.dictionary_apps.dtos.callback.response_dto import MessagerDTO
from dictionary.dictionary_apps.dtos.callback.request_dto import CreateMessageDTO

from dictionary.dictionary_apps.callback.services import MessageService
from dictionary.dictionary_apps.callback.repository import MessageRepository

from dictionary.dictionary_apps.users.models import BaseUser

class MessageCreateApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class InputSerializer(serializers.Serializer):
        user = serializers.IntegerField(required=False)
        text = serializers.CharField(required=False)
        telegram_id = serializers.IntegerField(required=False, default=0)
        # is_answered = serializers.CharField(required=False)
        # answer_text = serializers.CharField(required=False)
        # answered_at = serializers.CharField(required=False)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = user_get(serializer.validated_data['user'])
        serializer.validated_data['user'] = user
        print('SREVALDATA', serializer.validated_data)
        data = CreateMessageDTO(
            **serializer.validated_data,
        )
        message = MessageService(MessageRepository()).create_object(data)
        print(message)
        return Response(f'{message}')

class MessageDetailApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        user = serializers.CharField()
        text = serializers.CharField(required=False)
        is_answered = serializers.CharField(required=False)
        answer_text = serializers.CharField(required=False)
        answered_at = serializers.CharField(required=False)
        telegram_id = serializers.IntegerField(required=False)


    def get(self, request, message_id):
        message = message_get(message_id)
        if message is None:
            raise Http404
        dto = MessageService(MessageRepository()).detail_object(message)
        data = self.OutputSerializer(dto).data
        return Response(data)

class MessageListApi(LoginRequiredMixin, LimitOffsetPagination, APIView):

    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        user = serializers.IntegerField(required=False, allow_null=True)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = SiteMessage
            fields = ('id', 'user', 'text',
                    'is_answered', 'answer_text', 'created_at',
                    'answered_at', 'telegram_id',)
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        messages = MessageService(MessageRepository()).list_objects()
        return get_pagination_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=messages,
            request=request,
            view=self,
        )

class MessageUpdateApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class InputSerializer(serializers.Serializer):
        # user = serializers.IntegerField(required=False)
        # text = serializers.CharField(required=False)
        # is_answered = serializers.CharField(required=False)
        answer_text = serializers.CharField(required=False)
        # answered_at = serializers.CharField(required=False)

    def post(self, request, message_id):
        message = message_get(message_id)

        merged_data = {**MessageService(MessageRepository()).detail_object(message).__dict__, **request.data}
        serializer = self.InputSerializer(data=merged_data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['id'] = message_id
        serializer.validated_data['answered_at'] = datetime.now()
        serializer.validated_data['is_answered'] = True
        serializer.validated_data['user'] = message.user
        serializer.validated_data['created_at'] = message.created_at
        serializer.validated_data['text'] = message.text
        serializer.validated_data['telegarm_id'] = message.telegram_id

        dto = MessagerDTO(
           **serializer.validated_data
        )

        MessageService(MessageRepository()).update_object(dto)
        data = MessageDetailApi.OutputSerializer(message).data
        return Response(data)

class MessageDeleteApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = SiteMessage
            fields = ('id', 'user', 'text',
                    'is_answered', 'answer_text', 'created_at',
                    'answered_at', 'telegram_id',)
    def post(self, request, message_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        MessageService(MessageRepository()).delete_object(serializer.validated_data['id'])
        messages = MessageService(MessageRepository()).list_objects()
        return get_pagination_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=messages,
            request=request,
            view=self,
        )