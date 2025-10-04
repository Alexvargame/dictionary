from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin


from dictionary.dictionary_apps.api.pagination import (
    LimitOffsetPagination,
    get_pagination_response,
)

from dictionary.dictionary_apps.words.models import (Word, WordType, Noun, NounDeclensionsForm)

from dictionary.dictionary_apps.words.selectors import (word_type_get, noun_get, noundecl_get)
from dictionary.dictionary_apps.users.selectors import user_get

from dictionary.dictionary_apps.dtos.words.response_dto import NounDeclensionsFormDTO
from dictionary.dictionary_apps.dtos.words.request_dto import CreateNounDeclensionsFormDTO

from dictionary.dictionary_apps.words.services import NounDeclensionsFormService
from dictionary.dictionary_apps.words.repository import NounDeclensionsFormRepository




from dictionary.dictionary_apps.users.models import BaseUser


class OutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    noun = serializers.CharField()
    nominativ = serializers.CharField()
    akkusativ = serializers.CharField()
    dativ = serializers.CharField()
    genitiv = serializers.CharField()
    plural_nominativ = serializers.CharField()
    plural_akkusativ = serializers.CharField()
    plural_dativ = serializers.CharField()
    plural_genitiv = serializers.CharField()

class NounDeclensionsFormCreateApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class InputSerializer(serializers.Serializer):
        noun = serializers.IntegerField()
        nominativ = serializers.CharField()
        akkusativ = serializers.CharField()
        dativ = serializers.CharField()
        genitiv = serializers.CharField()
        plural_nominativ = serializers.CharField()
        plural_akkusativ = serializers.CharField()
        plural_dativ = serializers.CharField()
        plural_genitiv = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = CreateNounDeclensionsFormDTO(
            **serializer.validated_data,
        )
        word = NounDeclensionsFormService(NounDeclensionsFormRepository()).create_object(data)
        return Response(f'{word}')

class NounDeclensionsFormDetailApi(LoginRequiredMixin, LimitOffsetPagination, APIView):


    def get(self, request, noun_declensions_id):
        noun_declensions = noundecl_get(noun_declensions_id)
        if noun_declensions is None:
            raise Http404
        dto = NounDeclensionsFormService(NounDeclensionsFormRepository()).detail_object(noun_declensions)
        data = OutputSerializer(dto).data
        return Response(data)

class NounDeclensionsFormListApi(LoginRequiredMixin, LimitOffsetPagination, APIView):

    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        noun_declensions = NounDeclensionsFormService(NounDeclensionsFormRepository()).list_objects()
        return get_pagination_response(
            pagination_class=self.Pagination,
            serializer_class=OutputSerializer,
            queryset=noun_declensions,
            request=request,
            view=self,
        )

class NounDeclensionsFormUpdateApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class InputSerializer(serializers.Serializer):
        noun = serializers.IntegerField(allow_null=True,required=False)
        nominativ = serializers.CharField(required=False)
        akkusativ = serializers.CharField(required=False)
        dativ = serializers.CharField(required=False)
        genitiv = serializers.CharField(required=False)
        plural_nominativ = serializers.CharField(required=False)
        plural_akkusativ = serializers.CharField(required=False)
        plural_dativ = serializers.CharField(required=False)
        plural_genitiv = serializers.CharField(required=False)

    def post(self, request, noun_declensions_id):
        noun_declensions = noundecl_get(noun_declensions_id)
        merged_data = {**NounDeclensionsFormService(NounDeclensionsFormRepository()).detail_object(noun_declensions).__dict__, **request.data}
        if isinstance(merged_data.get('noun'), Noun):
            merged_data['noun'] = str(merged_data['noun'].id)
        serializer = self.InputSerializer(data=merged_data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['id'] = noun_declensions_id
        dto = NounDeclensionsFormDTO(
           **serializer.validated_data
        )

        NounDeclensionsFormService(NounDeclensionsFormRepository()).update_object(dto)
        data = OutputSerializer(noun_declensions).data
        return Response(data)

class NounDeclensionsFormDeleteApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
    class Pagination(LimitOffsetPagination):
        default_limit = 5

    def post(self, request, noun_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        NounDeclensionsFormService(NounDeclensionsFormRepository()).delete_object(serializer.validated_data['id'])
        noun_declensions = NounDeclensionsFormService(NounDeclensionsFormRepository()).list_objects()
        return get_pagination_response(
            pagination_class=self.Pagination,
            serializer_class=OutputSerializer,
            queryset=noun_declensions,
            request=request,
            view=self,
        )