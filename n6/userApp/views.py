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
from .models import Credential, User, UserRole


# example
class UserApiView(APIView):

    def get(self, request, formate=None):
        try:
            data = User.objects.values(
                'id', 'first_name', 'last_name', 'email_address', 'mobile_num')
            companyList = list(data)
            return Response({'status': status.HTTP_200_OK, 'msg': 'Company Data Fetched', 'data': companyList}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, formate=None):
        serializer = serializers.UserRegistrationSerializer(
            data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                json = serializer.data
                return Response({'status': status.HTTP_201_CREATED, 'msg': 'Company Created',  'data': json},
                                status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        user_id = request.data.get('id')
        try:
            # get the user object using the user ID
            user = User.objects.get(id=user_id)
            # replace `name` with the actual name field of your User model
        except User.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.UserRegistrationSerializer(
            user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'status': status.HTTP_200_OK, 'msg': 'User Data Updated', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
