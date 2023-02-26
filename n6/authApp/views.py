from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from . import serializers
from django.contrib.auth import authenticate
from .renderers import UserJSONRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from .models import User


# example
class UserRegistrationView(APIView):

    def get(self, request, formate=None):
        return Response({'msg': 'Registration Success'}, status=status.HTTP_201_CREATED)

    def post(self, request, formate=None):
        renderer_classes = [UserJSONRenderer]

        serializer = serializers.UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # token = get_tokens_for_user(user)
            if user:
                json = serializer.data
                return Response({'msg': 'Registration Success', 'token': 'token', 'data': json},
                                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyRegistrationView(APIView):

    def get(self, request, formate=None):
        return Response({'msg': 'Company Success'}, status=status.HTTP_201_CREATED)

    def post(self, request, formate=None):
        serializer = serializers.CompanyRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            company = serializer.save()
            if company:
                json = serializer.data
                return Response({'msg': 'Company Registration Success', 'token': 'token', 'data': json},
                                status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
