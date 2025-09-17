from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin


from dictionary.dictionary_apps.api.pagination import (
    LimitOffsetPagination,
    get_pagination_response,
)

from dictionary.dictionary_apps.words.models import Word, Lection, WordType, Pronoun

from dictionary.dictionary_apps.words.selectors import (lection_get, article_get,
                                                        word_type_get, pronoun_list,
                                                        pronoun_get)
from dictionary.dictionary_apps.users.selectors import user_get

from dictionary.dictionary_apps.dtos.words.response_dto import WordDTO, PronounDTO
from dictionary.dictionary_apps.dtos.words.request_dto import CreateWordDTO, CreatePronounDTO

from dictionary.dictionary_apps.words.services import WordService, PronounService
from dictionary.dictionary_apps.words.repository import WordRepository, PronounRepository



from dictionary.dictionary_apps.users.models import BaseUser



class PronounCreateApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class InputSerializer(serializers.Serializer):
        word_type = serializers.IntegerField()
        word = serializers.CharField()
        word_translate = serializers.CharField()
        lection = serializers.IntegerField()
        akkusativ = serializers.CharField()
        akkusativ_translate =serializers.CharField()
        dativ = serializers.CharField()
        dativ_translate = serializers.CharField()
        prossessive = serializers.CharField()
        prossessive_translate = serializers.CharField()
        reflexive = serializers.CharField()
        reflexive_translate = serializers.CharField()

    def post(self, request):
            serializer = self.InputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = CreatePronounDTO(
                **serializer.validated_data,
            )
            word = PronounService(PronounRepository()).create_object(data)
            return Response(f'{word}')

class PronounDetailApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        word_type = serializers.CharField()
        word = serializers.CharField()
        word_translate = serializers.CharField()
        lection = serializers.CharField()
        akkusativ = serializers.CharField()
        akkusativ_translate = serializers.CharField()
        dativ = serializers.CharField()
        dativ_translate = serializers.CharField()
        prossessive = serializers.CharField()
        prossessive_translate = serializers.CharField()
        reflexive = serializers.CharField()
        reflexive_translate = serializers.CharField()

    def get(self, request, pronoun_id):
        pronoun = pronoun_get(pronoun_id)
        if pronoun is None:
            raise Http404
        dto = PronounService(PronounRepository()).detail_object(pronoun)
        data = self.OutputSerializer(dto).data
        return Response(data)

class PronounListApi(LoginRequiredMixin, LimitOffsetPagination, APIView):

    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        lection = serializers.CharField(required=False, allow_null=True)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Pronoun
            fields = ('id', 'word', 'word_translate', 'lection',
                    'akkusativ', 'akkusativ_translate', 'dativ',
                    'dativ_translate', 'prossessive',
                    'prossessive_translate','reflexive',)

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        pronouns = PronounService(PronounRepository()).list_objects()
        return get_pagination_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=pronouns,
            request=request,
            view=self,
        )

class PronounUpdateApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class InputSerializer(serializers.Serializer):
        word_type = serializers.IntegerField(required=False, allow_null=True, default=1)
        word = serializers.CharField(required=False)
        akkusativ = serializers.CharField(required=False, allow_null=True, allow_blank=True)
        dativ = serializers.CharField(allow_blank=True, allow_null=True, required=False)
        prossessive = serializers.CharField(required=False, allow_null=True, allow_blank=True)
        reflexive = serializers.CharField(allow_blank=True, allow_null=True, required=False)
        akkusativ_translate = serializers.CharField(required=False, allow_null=True, allow_blank=True)
        dativ_translate = serializers.CharField(allow_blank=True, allow_null=True, required=False)
        prossessive_translate = serializers.CharField(required=False, allow_null=True, allow_blank=True)
        reflexive_translate = serializers.CharField(allow_blank=True, allow_null=True, required=False)
        word_translate = serializers.CharField(required=False)
        lection = serializers.IntegerField(required=False)
        declensions = serializers.JSONField(required=False)
        word_type = serializers.IntegerField()

    def post(self, request, pronoun_id):
        pronoun = pronoun_get(pronoun_id)

        merged_data = {**PronounService(PronounRepository()).detail_object(pronoun).__dict__, **request.data}
        if isinstance(merged_data.get('lection'), Lection):
            merged_data['lection'] = str(merged_data['lection'].id)
        if isinstance(merged_data.get('word_type'), WordType):
            merged_data['word_type'] = str(merged_data['word_type'].id)
        serializer = self.InputSerializer(data=merged_data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['id'] = pronoun_id
        dto = PronounDTO(
           **serializer.validated_data
        )
        PronounService(PronounRepository()).update_object(dto)
        pronoun= pronoun_get(pronoun_id)
        data = PronounDetailApi.OutputSerializer(pronoun).data
        return Response(data)

class PronounDeleteApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
    class Pagination(LimitOffsetPagination):
        default_limit = 5
    class OutputSerializer(serializers.ModelSerializer):

        class Meta:
            model = Pronoun
            fields = ('id', 'word', 'word_translate', 'lection',
                    'akkusativ', 'akkusativ_translate', 'dativ',
                    'dativ_translate', 'prossessive',
                    'prossessive_translate','reflexive',)

    def post(self, request, pronoun_id):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        PronounService(PronounRepository()).delete_object(serializer.validated_data['id'])
        pronouns = PronounService(PronounRepository()).list_objects()
        return get_pagination_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=pronouns,
            request=request,
            view=self,
        )