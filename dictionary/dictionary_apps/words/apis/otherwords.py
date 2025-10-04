from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin


from dictionary.dictionary_apps.api.pagination import (
    LimitOffsetPagination,
    get_pagination_response,
)

from dictionary.dictionary_apps.words.models import Word, WordType, OtherWords

from dictionary.dictionary_apps.words.selectors import (lection_get, word_type_get,
                                                        otherword_get
                                                       )
from dictionary.dictionary_apps.users.selectors import user_get

from dictionary.dictionary_apps.dtos.words.response_dto import WordDTO, OtherWordsDTO
from dictionary.dictionary_apps.dtos.words.request_dto import CreateWordDTO, CreateOtherWordsDTO

from dictionary.dictionary_apps.words.services import WordService, OtherWordsService
from dictionary.dictionary_apps.words.repository import WordRepository, OtherWordsRepository

from dictionary.dictionary_apps.users.models import BaseUser


class OutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    word_type = serializers.CharField()
    word = serializers.CharField()
    word_translate = serializers.CharField()
    lection = serializers.CharField()
class OtherWordsCreateApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class InputSerializer(serializers.Serializer):
        word_type = serializers.IntegerField()
        word = serializers.CharField()
        word_translate = serializers.CharField()
        lection = serializers.IntegerField(required=False)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = CreateVerbDTO(
            **serializer.validated_data,
        )
        word = VerbService(VerbRepository()).create_object(data)
        return Response(f'{word}')

class OtherWordsDetailApi(LoginRequiredMixin, LimitOffsetPagination, APIView):

    def get(self, request, ow_id):
        ow = otherword_get(ow_id)
        if ow is None:
            raise Http404
        dto = OtherWordsService(OtherWordsRepository()).detail_object(ow)
        data = OutputSerializer(dto).data
        return Response(data)

class OtherWordsListApi(LoginRequiredMixin, LimitOffsetPagination, APIView):

    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        lection = serializers.CharField(required=False, allow_null=True)

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        ows = OtherWordsService(OtherWordsRepository()).list_objects()
        return get_pagination_response(
            pagination_class=self.Pagination,
            serializer_class=OutputSerializer,
            queryset=ows,
            request=request,
            view=self,
        )

class OtherWordsUpdateApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class InputSerializer(serializers.Serializer):
        #word_type = serializers.IntegerField()
        word = serializers.CharField()
        word_translate = serializers.CharField()
        lection = serializers.IntegerField()


    def post(self, request, ow_id):
        ow = otherword_get(ow_id)

        merged_data = {**OtherWordsService(OtherWordsRepository()).detail_object(ow).__dict__, **request.data}
        if isinstance(merged_data.get('lection'), Lection):
            merged_data['lection'] = str(merged_data['lection'].id)
        if isinstance(merged_data.get('word_type'), WordType):
            merged_data['word_type'] = str(merged_data['word_type'].id)
        serializer = self.InputSerializer(data=merged_data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['id'] = ow_id
        dto = VerbDTO(
           **serializer.validated_data
        )

        OtherWordsService(OtherWordsRepository()).update_object(dto)
        data = OutputSerializer(ow).data
        return Response(data)

class OtherWordsDeleteApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
    class Pagination(LimitOffsetPagination):
        default_limit = 5

    def post(self, request, noun_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        OtherWordsService(OtherWordsRepository()).delete_object(serializer.validated_data['id'])
        ows = OtherWordsService(OtherWordsRepository()).list_objects()
        return get_pagination_response(
            pagination_class=self.Pagination,
            serializer_class=OutputSerializer,
            queryset=ows,
            request=request,
            view=self,
        )