from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin


from dictionary.dictionary_apps.api.pagination import (
    LimitOffsetPagination,
    get_pagination_response,
)

from dictionary.dictionary_apps.words.models import Word, Lection, WordType, Adjective

from dictionary.dictionary_apps.words.selectors import (lection_get, article_get,
                                                        word_type_get, adjective_get)
from dictionary.dictionary_apps.users.selectors import user_get

from dictionary.dictionary_apps.dtos.words.response_dto import WordDTO, AdjectiveDTO
from dictionary.dictionary_apps.dtos.words.request_dto import CreateWordDTO, CreateAdjectiveDTO

from dictionary.dictionary_apps.words.services import WordService, AdjectiveService
from dictionary.dictionary_apps.words.repository import WordRepository, AdjectiveRepository



from dictionary.dictionary_apps.users.models import BaseUser



class AdjectiveCreateApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class InputSerializer(serializers.Serializer):
        word_type = serializers.IntegerField()
        word = serializers.CharField()
        word_translate = serializers.CharField()
        lection = serializers.IntegerField()
        komparativ = serializers.CharField()
        superlativ = serializers.CharField()
        declensions = serializers.JSONField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = CreateAdjectiveDTO(
            **serializer.validated_data,
        )
        word = AdjectiveService(AdjectiveRepository()).create_object(data)
        return Response(f'{word}')

class AdjectiveDetailApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        word_type = serializers.CharField()
        word = serializers.CharField()
        word_translate = serializers.CharField()
        lection = serializers.CharField()
        komparativ = serializers.CharField()
        superlativ = serializers.CharField()
        declensions = serializers.JSONField()

    def get(self, request, adjective_id):
        adjective = adjective_get(adjective_id)
        if adjective is None:
            raise Http404
        dto = AdjectiveService(AdjectiveRepository()).detail_object(adjective)
        data = self.OutputSerializer(dto).data
        return Response(data)

class AdjectiveListApi(LoginRequiredMixin, LimitOffsetPagination, APIView):

    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        lection = serializers.CharField(required=False, allow_null=True)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Adjective
            fields = ('id', 'word', 'word_translate', 'lection',
                    'komparativ', 'superlativ', 'declensions' )
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        adjectives = AdjectiveService(AdjectiveRepository()).list_objects()
        return get_pagination_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=adjectives,
            request=request,
            view=self,
        )

class AdjectiveUpdateApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class InputSerializer(serializers.Serializer):
        word_type = serializers.IntegerField(required=False, allow_null=True, default=1)
        word = serializers.CharField(required=False)
        komparativ = serializers.CharField(required=False, allow_null=True, allow_blank=True)
        superlativ = serializers.CharField(allow_blank=True, allow_null=True, required=False)
        word_translate = serializers.CharField(required=False)
        lection = serializers.IntegerField(required=False)
        declensions = serializers.JSONField(required=False)
    def post(self, request, adjective_id):
        adjective = adjective_get(adjective_id)

        merged_data = {**AdjectiveService(AdjectiveRepository()).detail_object(adjective).__dict__, **request.data}
        if isinstance(merged_data.get('lection'), Lection):
            merged_data['lection'] = str(merged_data['lection'].id)
        if isinstance(merged_data.get('word_type'), WordType):
            merged_data['word_type'] = str(merged_data['word_type'].id)
        serializer = self.InputSerializer(data=merged_data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['id'] = adjective_id
        dto = AdjectiveDTO(
           **serializer.validated_data
        )
        AdjectiveService(AdjectiveRepository()).update_object(dto)
        adjective = adjective_get(adjective_id)
        data = AdjectiveDetailApi.OutputSerializer(adjective).data
        return Response(data)

class AdjectiveDeleteApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
    class Pagination(LimitOffsetPagination):
        default_limit = 5
    class OutputSerializer(serializers.ModelSerializer):

        class Meta:
            model = Adjective
            fields = ('id', 'word', 'word_translate', 'lection',
                    'komparativ', 'superlativ', 'declensions' )
    def post(self, request, adjective_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        AdjectiveService(AdjectiveRepository()).delete_object(serializer.validated_data['id'])
        adjectives = AdjectiveService(AdjectiveRepository()).list_objects()
        return get_pagination_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=adjectives,
            request=request,
            view=self,
        )