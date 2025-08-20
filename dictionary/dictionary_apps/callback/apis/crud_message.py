from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin


from dictionary.dictionary_apps.api.pagination import (
    LimitOffsetPagination,
    get_pagination_response,
)

from dictionary.dictionary_apps.callback.models import SiteMessage

from dictionary.dictionary_apps.callback.selectors import (message_list)
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

class VerbDetailApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        word_type = serializers.IntegerField()
        word = serializers.CharField()
        word_translate = serializers.CharField()
        ich_form = serializers.CharField()
        du_form = serializers.CharField()
        er_sie_es_form = serializers.CharField()
        wir_form = serializers.CharField()
        ihr_form = serializers.CharField()
        Sie_sie_form = serializers.CharField()
        past_perfect_form = serializers.CharField()
        past_prateritum_ich_form = serializers.CharField()
        past_prateritum_du_form = serializers.CharField()
        past_prateritum_er_sie_es_form = serializers.CharField()
        past_prateritum_wir_form = serializers.CharField()
        past_prateritum_ihr_form = serializers.CharField()
        past_prateritum_Sie_sie_form = serializers.CharField()
        lection = serializers.IntegerField()


    def get(self, request, verb_id):
        verb = verb_get(verb_id)
        if verb is None:
            raise Http404
        dto = VerbService(VerbRepository()).detail_object(verb)
        data = self.OutputSerializer(dto).data
        return Response(data)

# class VerbListApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
#
#     class Pagination(LimitOffsetPagination):
#         default_limit = 5
#
#     class FilterSerializer(serializers.Serializer):
#         id = serializers.IntegerField(required=False)
#         lection = serializers.CharField(required=False, allow_null=True)
#
#     class OutputSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = Verb
#             fields = ('id', 'word', 'word_translate',
#                     'ich_form', 'du_form', 'er_sie_es_form',
#                     'wir_form', 'ihr_form', 'Sie_sie_form',
#                     'past_perfect_form', 'past_pratertium_ich_form',
#                       'past_prateritum_du_form', 'past_prateritum_er_sie_es_form',
#                       'past_prateritum_wir_form', 'past_prateritum_ihr_form',
#                       'past_prateritum_Sie_sie_form', 'lection', 'word_type',)
#     def get(self, request):
#         filters_serializer = self.FilterSerializer(data=request.query_params)
#         filters_serializer.is_valid(raise_exception=True)
#         verbs = VerbService(VerbRepository()).list_objects()
#         return get_pagination_response(
#             pagination_class=self.Pagination,
#             serializer_class=self.OutputSerializer,
#             queryset=verbs,
#             request=request,
#             view=self,
#         )
#
# class VerbUpdateApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
#     class InputSerializer(serializers.Serializer):
#         word_type = serializers.IntegerField()
#         word = serializers.CharField()
#         word_translate = serializers.CharField()
#         ich_form = serializers.CharField()
#         du_form = serializers.CharField()
#         er_sie_es_form = serializers.CharField()
#         wir_form = serializers.CharField()
#         ihr_form = serializers.CharField()
#         Sie_sie_form = serializers.CharField()
#         past_perfect_form = serializers.CharField()
#         past_prateritum_ich_form = serializers.CharField(required=False)
#         past_prateritum_du_form = serializers.CharField(required=False)
#         past_prateritum_er_sie_es_form = serializers.CharField(required=False)
#         past_prateritum_wir_form = serializers.CharField(required=False)
#         past_prateritum_ihr_form = serializers.CharField(required=False)
#         past_prateritum_Sie_sie_form = serializers.CharField(required=False)
#         lection = serializers.IntegerField()
#
#
#     def post(self, request, verb_id):
#         verb = verb_get(verb_id)
#
#         merged_data = {**VerbService(VerbRepository()).detail_object(noun).__dict__, **request.data}
#         if isinstance(merged_data.get('lection'), Lection):
#             merged_data['lection'] = str(merged_data['lection'].id)
#         if isinstance(merged_data.get('word_type'), WordType):
#             merged_data['word_type'] = str(merged_data['word_type'].id)
#         serializer = self.InputSerializer(data=merged_data)
#         serializer.is_valid(raise_exception=True)
#         serializer.validated_data['id'] = noun_id
#         dto = VerbDTO(
#            **serializer.validated_data
#         )
#
#         VerbService(VerbRepository()).update_object(dto)
#         data = VerbDetailApi.OutputSerializer(verb).data
#         return Response(data)
#
# class VerbDeleteApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
#     class InputSerializer(serializers.Serializer):
#         id = serializers.IntegerField()
#     class Pagination(LimitOffsetPagination):
#         default_limit = 5
#
#     def post(self, request, noun_id):
#         serializer = self.InputSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         VerbService(VerbRepository()).delete_object(serializer.validated_data['id'])
#         verbs = VerbService(VerbRepository()).list_objects()
#         return get_pagination_response(
#             pagination_class=self.Pagination,
#             serializer_class=self.OutputSerializer,
#             queryset=verbs,
#             request=request,
#             view=self,
#         )