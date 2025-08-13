from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin




class CallBackTelegram(LoginRequiredMixin, APIView):
    print('TELCALL')