from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin


from dictionary.dictionary_apps.api.pagination import (
    LimitOffsetPagination,
    get_pagination_response,
)

from dictionary.dictionary_apps.words.models import Word, Lection, Article, WordType, Noun

from dictionary.dictionary_apps.words.selectors import (lection_get, article_get,
                                                        word_type_get, noun_get)
from dictionary.dictionary_apps.users.selectors import user_get

from dictionary.dictionary_apps.dtos.words.response_dto import WordDTO, NounDTO
from dictionary.dictionary_apps.dtos.words.request_dto import CreateWordDTO, CreateNounDTO

from dictionary.dictionary_apps.words.services import WordService, NounService
from dictionary.dictionary_apps.words.repository import WordRepository, NounRepository




from dictionary.dictionary_apps.users.models import BaseUser

# class WordCreateApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
#     class InputSerializer(serializers.Serializer):
#         word_type = serializers.IntegerField()
#         lection = serializers.IntegerField()
#
#     def post(self, request):
#         serializer = self.InputSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         lection = lection_get(serializer.validated_data['lection'])
#         serializer.validated_data['lection'] = lection
#         word_type = word_type_get(serializer.validated_data['word_type'])
#         serializer.validated_data['word_type'] = word_type
#
#         data = CreateWordDTO(
#             **serializer.validated_data,
#         )
#         word = WordService(WordRepository()).create_object(data)
#         data = WordDetailApi.OutputSerializer(word).data
#         return Response(data)

# class WordDetailApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
#     class OutputSerializer(serializers.Serializer):
#         id = serializers.IntegerField()
#         word_single = serializers.CharField()
#         word_plural = serializers.CharField()
#         plural_sign = serializers.CharField(allow_blank=True, allow_null=True, required=False)
#         word_translate = serializers.CharField()
#         word_translate_plural = serializers.CharField()
#         lection = serializers.CharField()
#         #book = serializers.IntegerField()
#         article = serializers.CharField()
#
#     def get(self, request, word_id):
#         word = word_get(word_id)
#         if word is None:
#             raise Http404
#         dto = WordService(WordRepository()).detail_object(word)
#         data = self.OutputSerializer(dto).data
#         return Response(data)
#
#
# class WordListApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
#
#     class Pagination(LimitOffsetPagination):
#         default_limit = 2
#
#     class FilterSerializer(serializers.Serializer):
#         id = serializers.IntegerField(required=False)
#         lection = serializers.CharField(required=False, allow_null=True)
#         article = serializers.CharField(required=False)
#
#     class OutputSerializer(serializers.ModelSerializer):
#
#         class Meta:
#             model = Word
#             fields = ('id', 'id', 'word_single', 'word_plural', 'word_translate',
#                     'word_translate_plural','lection', 'article')
#     def get(self, request):
#         filters_serializer = self.FilterSerializer(data=request.query_params)
#         filters_serializer.is_valid(raise_exception=True)
#         words = WordService(WordRepository()).list_objects()
#         return get_pagination_response(
#             pagination_class=self.Pagination,
#             serializer_class=self.OutputSerializer,
#             queryset=words,
#             request=request,
#             view=self,
#         )
#
#
# class WordUpdateApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
#     class InputSerializer(serializers.Serializer):
#         word_single = serializers.CharField(required=False)
#         word_plural = serializers.CharField(required=False)
#         plural_sign = serializers.CharField(allow_blank=True, allow_null=True, required=False)
#         word_translate = serializers.CharField(required=False)
#         word_translate_plural = serializers.CharField(required=False)
#         lection = serializers.CharField(allow_blank=True, allow_null=True, required=False)
#         article = serializers.CharField(allow_blank=True, allow_null=True, required=False)
#
#     def post(self, request, word_id):
#         word = word_get(word_id)
#         print('WORD', word)
#
#         merged_data = {**WordService(WordRepository()).detail_object(word).__dict__, **request.data}
#         if isinstance(merged_data.get('lection'), Lection):
#             merged_data['lection'] = str(merged_data['lection'].id)
#         if isinstance(merged_data.get('article'), Article):
#             merged_data['article'] = str(merged_data['article'].id)
#         serializer = self.InputSerializer(data=merged_data)
#         serializer.is_valid(raise_exception=True)
#         serializer.validated_data['id'] = word_id
#         dto = WordDTO(
#            **serializer.validated_data
#         )
#         WordService(WordRepository()).update_object(dto)
#         word = word_get(word_id)
#         data = WordDetailApi.OutputSerializer(word).data
#         return Response(data)
#
# class WordDeleteApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
#     class InputSerializer(serializers.Serializer):
#         id = serializers.IntegerField()
#     class Pagination(LimitOffsetPagination):
#         default_limit = 2
#     class OutputSerializer(serializers.ModelSerializer):
#
#         class Meta:
#             model = Word
#             fields = ('id', 'id', 'word_single', 'word_plural', 'word_translate',
#                     'word_translate_plural','lection', 'article')
#     def post(self, request, word_id):
#         serializer = self.InputSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         WordService(WordRepository()).delete_object(serializer.validated_data['id'])
#         words = WordService(WordRepository()).list_objects()
#         # data = self.OutputSerializer(query, many=True).data
#         return get_pagination_response(
#             pagination_class=self.Pagination,
#             serializer_class=self.OutputSerializer,
#             queryset=words,
#             request=request,
#             view=self,
#         )
class OutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    word = serializers.CharField()
    word_type = serializers.CharField()
    word_plural = serializers.CharField()
    plural_sign = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    word_translate = serializers.CharField()
    word_translate_plural = serializers.CharField()
    lection = serializers.CharField()
    article = serializers.CharField()
class NounCreateApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class InputSerializer(serializers.Serializer):
        word_type = serializers.IntegerField()
        word = serializers.CharField()
        word_plural = serializers.CharField()
        plural_sign = serializers.CharField(allow_blank=True, allow_null=True, required=False)
        word_translate = serializers.CharField()
        word_translate_plural = serializers.CharField()
        article = serializers.IntegerField()
        lection = serializers.IntegerField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = CreateNounDTO(
            **serializer.validated_data,
        )
        word = NounService(NounRepository()).create_object(data)
        return Response(f'{word}')

class NounDetailApi(LoginRequiredMixin, LimitOffsetPagination, APIView):

    def get(self, request, noun_id):
        noun = noun_get(noun_id)
        if noun is None:
            raise Http404
        dto = NounService(NounRepository()).detail_object(noun)
        data = OutputSerializer(dto).data
        return Response(data)

class NounListApi(LoginRequiredMixin, LimitOffsetPagination, APIView):

    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        lection = serializers.CharField(required=False, allow_null=True)
        article = serializers.CharField(required=False)

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        nouns = NounService(NounRepository()).list_objects()
        return get_pagination_response(
            pagination_class=self.Pagination,
            serializer_class=OutputSerializer,
            queryset=nouns,
            request=request,
            view=self,
        )

class NounUpdateApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class InputSerializer(serializers.Serializer):
        #word_type = serializers.IntegerField(required=False, allow_null=True, default=1)
        word = serializers.CharField(required=False)
        word_plural = serializers.CharField(required=False)
        plural_sign = serializers.CharField(allow_blank=True, allow_null=True, required=False)
        word_translate = serializers.CharField(required=False)
        word_translate_plural = serializers.CharField(required=False)
        lection = serializers.IntegerField(allow_null=True, required=False)# allow_blank=True,
        article = serializers.IntegerField(allow_null=True,required=False)

        # word_type = serializers.PrimaryKeyRelatedField(
        #     queryset=WordType.objects.all(),
        #     required=False,
        #     allow_null=True,
        #     default=1
        # )
    def post(self, request, noun_id):
        print(request.data)
        noun = noun_get(noun_id)

        merged_data = {**NounService(NounRepository()).detail_object(noun).__dict__, **request.data}
        if isinstance(merged_data.get('lection'), Lection):
            merged_data['lection'] = str(merged_data['lection'].id)
        if isinstance(merged_data.get('article'), Article):
            merged_data['article'] = str(merged_data['article'].id)
        if isinstance(merged_data.get('word_type'), WordType):
            merged_data['word_type'] = str(merged_data['word_type'].id)
        print(merged_data)
        serializer = self.InputSerializer(data=merged_data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['id'] = noun_id
        dto = NounDTO(
           **serializer.validated_data
        )

        NounService(NounRepository()).update_object(dto)
        data = OutputSerializer(noun).data
        return Response(data)

class NounDeleteApi(LoginRequiredMixin, LimitOffsetPagination, APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
    class Pagination(LimitOffsetPagination):
        default_limit = 5

    def post(self, request, noun_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(
            serializer.validated_data['id']
        )
        NounService(NounRepository()).delete_object(serializer.validated_data['id'])
        nouns = NounService(NounRepository()).list_objects()
        return get_pagination_response(
            pagination_class=self.Pagination,
            serializer_class=OutputSerializer,
            queryset=nouns,
            request=request,
            view=self,
        )