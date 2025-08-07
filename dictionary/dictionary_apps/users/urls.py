from django.urls import path

from .apis import UserCreateApi, UserUpdateApi, UserDetailApi, UserListApi
from .auth_function import register, login_view, logout_view

app_name = 'users'
urlpatterns =[
    path('create/', UserCreateApi.as_view(), name='user_create'),
    path('<int:user_id>/', UserDetailApi.as_view(), name='user_detail'),
    path('', UserListApi.as_view(), name='users_list'),
    path('<int:user_id>/update/', UserUpdateApi.as_view(), name='user_update'),
    path('register/', register, name='user_registration'),
    path('login/', login_view, name='user_login'),
    path('logout/', logout_view, name='user_logout'),

    # path('fr/<int:user_id>/', UserDetailApiFrontEnd.as_view(), name='user_detail_frontend'),
    # path('fr/<int:user_id>/list/', UserPropertyListApiFrontEnd.as_view(), name='user_list_objects'),

]