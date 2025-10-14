from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.core.paginator import Paginator


from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

from dictionary.dictionary_apps.api.pagination import (
    LimitOffsetPagination,
    get_pagination_response,
)


from dictionary.dictionary_apps.users.models import BaseUser, UserRole
from dictionary.dictionary_apps.users.selectors import user_get, user_role_get

from dictionary.dictionary_apps.users.services import UsersService, UserRoleService
from dictionary.dictionary_apps.users.repository import UsersRepository, UserRoleRepository
from dictionary.dictionary_apps.dtos.users.request_dto import CreateUserDTO, CreateUserRoleDTO
from dictionary.dictionary_apps.dtos.users.response_dto import UserDTO, UserRoleDTO

#

# class UserDetailApiFrontEnd(LimitOffsetPagination, APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'users/user_detail.html'
#
#     class OutputSerializer(serializers.Serializer):
#         id = serializers.IntegerField()
#         email = serializers.EmailField()
#         password = serializers.CharField()
#         username = serializers.CharField()
#         is_admin = serializers.BooleanField()
#         is_active = serializers.BooleanField()
#         name = serializers.CharField()
#         surname = serializers.CharField()
#         phone = serializers.CharField()
#         #добваить как объект, а не iDs
#         user_role = serializers.CharField()
#     def get(self, request, user_id):
#         user = user_get(user_id)
#         if user is None:
#             raise Http404
#         dto = UsersService(UsersRepository()).detail_object(user)
#         data = self.OutputSerializer(dto).data
#         return  Response({'data': property, 'obj': dto})
#
# #

class UserFrontListApi(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'users/users_for_admin.html'
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        user_role = serializers.IntegerField(required=False, allow_null=True, default=None)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        surname = serializers.CharField()
        username = serializers.CharField()
        email = serializers.EmailField()
        is_active = serializers.BooleanField()
        is_admin = serializers.BooleanField()
        user_role = serializers.CharField(source='user_role.name')
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        filter_data = filters_serializer.validated_data
        users = UsersService(UsersRepository()).list_objects()
        if 'email' in filter_data:
            users = [u for u in users if filter_data['email'].lower() in u.email.lower()]
        if 'user_role' in filter_data and filter_data['user_role'] is not None:
            users = [u for u in users if u.user_role.id == filter_data['user_role']]
        paginator = Paginator(users, self.Pagination.default_limit)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        serialized_users = self.OutputSerializer(page_obj.object_list, many=True).data
        roles = UserRoleService(UserRoleRepository()).list_objects()
        print(roles)
        context = {
            'users': serialized_users,  # для таблицы
            'roles': roles,
            'is_paginated': page_obj.has_other_pages(),
            'page_obj': page_obj,  # для кнопок "Назад/Вперед"
        }
        return render(request, 'users/users_for_admin.html', context)

        # return get_pagination_response(
        #     pagination_class=self.Pagination,
        #     serializer_class=self.OutputSerializer,
        #     queryset=users,
        #     request=request,
        #     view=self,
        # )



# class UserFrontUpdateApi(LoginRequiredMixin, APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'users/profile.html'
#
#     class OutputSerializer(serializers.Serializer):
#         id = serializers.IntegerField()
#         name = serializers.CharField()
#         surname = serializers.CharField()
#         email = serializers.EmailField()
#         phone = serializers.CharField()
#         telegram_username = serializers.CharField()
#         last_login_date = serializers.DateTimeField()
#         is_active = serializers.BooleanField()
#         is_admin = serializers.BooleanField()
#         user_role = serializers.CharField()
#         chat_id = serializers.IntegerField()
#         score = serializers.IntegerField()
#         lifes = serializers.IntegerField()
#         username = serializers.CharField()
#         registration_date = serializers.DateTimeField()
#     class InputSerializer(serializers.Serializer):
#         name = serializers.CharField(required=False, allow_blank=True)
#         surname = serializers.CharField(required=False, allow_blank=True)
#         email = serializers.EmailField(required=False)
#         phone = serializers.CharField(required=False, allow_blank=True)
#         telegram_username = serializers.CharField(required=False, allow_blank=True)
#
#     def get(self, request, user_id):
#         user = user_get(user_id)
#         data = self.OutputSerializer(user).data
#         context = {
#             'user': data,
#         }
#         return Response(context)
#     def post(self, request, user_id):
#         user = user_get(user_id)
#         if not user:
#             raise Http404
#         raw_data = request.data.dict() if hasattr(request.data, 'dict') else request.data
#         merged_data = {**UsersService(UsersRepository()).detail_object(user).__dict__, **raw_data}
#         serializer = self.InputSerializer(data=merged_data)
#         serializer.is_valid(raise_exception=True)
#
#
#         serializer.validated_data['id'] = user.id
#         serializer.validated_data['user_role'] = user.user_role.id
#         serializer.validated_data['is_admin'] = user.is_admin
#         serializer.validated_data['is_active'] = user.is_active
#         serializer.validated_data['username'] = user.username
#         serializer.validated_data['registration_date'] =user.registration_date
#         serializer.validated_data['last_login_date'] = user.last_login_date
#         serializer.validated_data['chat_id'] = user.chat_id
#         serializer.validated_data['score'] = user.score
#         serializer.validated_data['lifes'] = user.lifes
#         serializer.validated_data['password'] = user.password
#         dto = UserDTO(
#            **serializer.validated_data
#         )
#         UsersService(UsersRepository()).update_object(dto)
#         user = user_get(user_id)
#         data = self.OutputSerializer(user).data
#         context ={
#             'user': data,
#         }
#         return Response(context)



class UserFrontUpdateApi(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'users/profile.html'

    # Serializer для отображения всех полей
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        surname = serializers.CharField()
        email = serializers.EmailField()
        phone = serializers.CharField()
        telegram_username = serializers.CharField()
        last_login_date = serializers.DateTimeField()
        is_active = serializers.BooleanField()
        is_admin = serializers.BooleanField()
        user_role = serializers.CharField()
        chat_id = serializers.IntegerField()
        score = serializers.IntegerField()
        lifes = serializers.IntegerField()
        username = serializers.CharField()
        registration_date = serializers.DateTimeField()

    # Serializer только для редактируемых полей
    class UserInputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False, allow_blank=True)
        surname = serializers.CharField(required=False, allow_blank=True)
        email = serializers.EmailField(required=False)
        phone = serializers.CharField(required=False, allow_blank=True)
        telegram_username = serializers.CharField(required=False, allow_blank=True)

    class AdminInputSerializer(UserInputSerializer):
        is_active = serializers.BooleanField(required=False)
        is_admin = serializers.BooleanField(required=False)
        score = serializers.IntegerField(required=False)
        lifes = serializers.IntegerField(required=False)
        user_role = serializers.IntegerField(required=False)

    def get_serializer_class(self, request, target_user):
        if request.user.is_admin:
            return self.AdminInputSerializer
        return self.UserInputSerializer
    def get(self, request, user_id):
        user = user_get(user_id)
        if not user:
            return Response({'error': "User not found"}, status=404)
        serializer = self.OutputSerializer(user)
        is_admin_editing = request.user.is_admin and request.user.id != user.id
        roles = UserRoleService(UserRoleRepository()).list_objects()
        return Response({
            'user_profile': serializer.data,
            'is_admin_editing': is_admin_editing,
            'roles': roles,
        })

    def post(self, request, user_id):
        print(request.POST)
        user = user_get(user_id)
        SericalizerClass = self.get_serializer_class(request, user)
        serializer = SericalizerClass(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Берем DTO исходные данные и обновляем только разрешённые поля
        dto_data = UsersService(UsersRepository()).detail_object(user).__dict__.copy()
        # Исключаем служебные поля, которые не нужны DTO
        dto_data.pop('_state', None)

        for field, value in serializer.validated_data.items():
            dto_data[field] = value
        dto_data['user_role'] = user_role_get(dto_data['user_role'])
        if dto_data['user_role'].id == 1:
            dto_data['is_admin'] = True
        else:
            dto_data['is_admin'] = False
        # Создаем DTO
        dto = UserDTO(**dto_data)
        UsersService(UsersRepository()).update_object(dto)
        # Получаем свежие данные
        updated_user = user_get(user_id)
        is_admin_editing = bool(getattr(request.user, 'is_admin', False) and request.user.id != updated_user.id)
        roles = UserRoleService(UserRoleRepository()).list_objects()
        return Response({
            'user_profile': self.OutputSerializer(updated_user).data,
            'is_admin_editing': is_admin_editing,
            'roles': roles,
        })


#
#
