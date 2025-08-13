from django.urls import include, path

from .views import main_page
urlpatterns =[

    path('', main_page, name='main_page'),

    path('users/', include(('dictionary.dictionary_apps.users.urls', 'users'), namespace='users')),
    path('words/', include(('dictionary.dictionary_apps.words.urls','words'), namespace='words')),
    path('exercises/', include(('dictionary.dictionary_apps.exercises.urls','exercises'), namespace='exercises')),
    path('callback/', include(('dictionary.dictionary_apps.callback.urls', 'callback'), namespace='callback')),
    # #path('propertys/', include('estate_agency.estate_agency_apps.property.urls')),
    # path('propertys/', include(('estate_agency.estate_agency_apps.property.urls', 'propertys'), namespace='propertys')),
    # path('property_searches/', include('estate_agency.estate_agency_apps.property_search.urls', 'property_searches')),
    # path('clients/', include('estate_agency.estate_agency_apps.clients.urls', 'clients')),
]