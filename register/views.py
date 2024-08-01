from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .serializers import CreateUserSerializer

class Register(CreateAPIView):

    serializer_class = CreateUserSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()
 