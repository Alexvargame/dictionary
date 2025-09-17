from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin


from dictionary.dictionary_apps.api.pagination import (
    LimitOffsetPagination,
    get_pagination_response,
)

from dictionary.dictionary_apps.words.models import Word, Lection, WordType, Numeral

from dictionary.dictionary_apps.words.selectors import (lection_get, numeral_get,
                                                        word_type_get)
from dictionary.dictionary_apps.users.selectors import user_get

from dictionary.dictionary_apps.dtos.words.response_dto import WordDTO, NumeralDTO
from dictionary.dictionary_apps.dtos.words.request_dto import CreateWordDTO, CreateNumeralDTO

from dictionary.dictionary_apps.words.services import WordService, NumeralService
from dictionary.dictionary_apps.words.repository import WordRepository, NumeralRepository




from dictionary.dictionary_apps.users.models import BaseUser



class NumeralCreateApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class InputSerializer(serializers.Serializer):
        word_type = serializers.IntegerField()
        word = serializers.CharField()
        word_translate = serializers.CharField()
        ordinal = serializers.CharField()
        date_numeral = serializers.CharField()
        lection = serializers.IntegerField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # lection = lection_get(serializer.validated_data['lection'])
        # serializer.validated_data['lection'] = lection
        # word_type = word_type_get(serializer.validated_data['word_type'])
        # serializer.validated_data['word_type'] = word_type

        data = CreateNumeralDTO(
            **serializer.validated_data,
        )
        word = NumeralService(NumeralRepository()).create_object(data)
        #data = WordDetailApi.OutputSerializer(word).data
        return Response(f'{word}')

class NumearalDetailApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        word_type = serializers.CharField()
        word = serializers.CharField()
        word_translate = serializers.CharField()
        ordinal = serializers.CharField()
        date_numeral = serializers.CharField()
        lection = serializers.CharField()

    def get(self, request, numeral_id):
        numeral = numeral_get(numeral_id)
        if numeral is None:
            raise Http404
        dto = NumeralService(NumeralRepository()).detail_object(numeral)
        data = self.OutputSerializer(dto).data
        return Response(data)

class NumeralListApi(LoginRequiredMixin, LimitOffsetPagination, APIView):

    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        lection = serializers.CharField(required=False, allow_null=True)
        article = serializers.CharField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Numeral
            fields = ('id',  'word_type', 'word', 'ordinal', 'date_numeral',
                    'lection', )
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        numerals = NumeralService(NumeralRepository()).list_objects()
        return get_pagination_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=numerals,
            request=request,
            view=self,
        )

class NumeralUpdateApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class InputSerializer(serializers.Serializer):
        word_type = serializers.IntegerField(required=False, allow_null=True, default=1)
        word = serializers.CharField(required=False)
        ordinal = serializers.CharField(required=False)
        date_numeral = serializers.CharField(allow_blank=True, allow_null=True, required=False)
        word_translate = serializers.CharField(required=False)
        lection = serializers.IntegerField(allow_null=True, required=False)

    def post(self, request, numeral_id):
        numeral = numeral_get(numeral_id)

        merged_data = {**NumeralService(NumeralRepository()).detail_object(numeral).__dict__, **request.data}
        if isinstance(merged_data.get('lection'), Lection):
            merged_data['lection'] = str(merged_data['lection'].id)
        if isinstance(merged_data.get('word_type'), WordType):
            merged_data['word_type'] = str(merged_data['word_type'].id)
        serializer = self.InputSerializer(data=merged_data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['id'] = numeral_id
        dto = NumeralDTO(
           **serializer.validated_data
        )
        NumeralService(NumeralRepository()).update_object(dto)
        numeral = numeral_get(numeral_id)
        data = NumearalDetailApi.OutputSerializer(numeral).data
        return Response(data)

class NumeralDeleteApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
    class Pagination(LimitOffsetPagination):
        default_limit = 5
    class OutputSerializer(serializers.ModelSerializer):

        class Meta:
            model = Numeral
            fields = ('id',  'word_type', 'word', 'ordinal', 'date_numeral',
                    'lection', )
    def post(self, request, numeral_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        NumeralService(NumeralRepository()).delete_object(serializer.validated_data['id'])
        numerals = NumeralService(NumeralRepository()).list_objects()
        return get_pagination_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=numerals,
            request=request,
            view=self,
        )