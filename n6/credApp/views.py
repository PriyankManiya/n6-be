from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from credApp.models import Credential
from . import serializers
from userApp.models import UserRole, User
from companyApp.models import Company
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class CredListApiView(APIView):

    def get(self, request, formate=None):
        try:
            data = Credential.objects.values(
                'id', 'user_name', 'active_tf', 'user_id', 'user_level_id')
            temp = []

            for obj in data:
                user_role_id = obj['user_level_id']
                user_id = obj['user_id']
                userRole = UserRole.objects.get(id=int(user_role_id))
                user = User.objects.get(id=int(user_id))

                temp.append(
                    {
                        **obj,
                        'user_level_id': user_role_id,
                        'user_level': {
                            'role': userRole.role
                        },
                        'user_id': user_id,
                        'user': {
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'email_address': user.email_address,
                            'mobile_num': user.mobile_num,
                            'company': {
                                'name': user.company.name,
                                'email_address': user.company.email_address,
                                'mobile_num': user.company.mobile_num,
                            }

                        }
                    })

            credList = list(temp)
            credList.sort(key=lambda temp: -temp['id'])
            return Response({'status': status.HTTP_200_OK, 'msg': 'Creds Data Fetched', 'data': credList}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)


class CredApiView(APIView):

    def get(self, request, formate=None):
        try:
            cred_id = request.data.get('id')
            cred = Credential.objects.get(id=int(cred_id))
            serializer = serializers.CredentialAppSerializer(
                cred, data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                cred = serializer.data

                user_role_id = cred['user_level']
                user_id = cred['user']
                userRole = UserRole.objects.get(id=int(user_role_id))
                user = User.objects.get(id=int(user_id))

                temp = {
                    **cred,
                    'user_level_id': user_role_id,
                    'user_level': {
                        'role': userRole.role
                    },
                    'user_id': user_id,
                    'user': {
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email_address': user.email_address,
                        'mobile_num': user.mobile_num,
                        'company': {
                            'name': user.company.name,
                            'email_address': user.company.email_address,
                            'mobile_num': user.company.mobile_num,
                        }
                    }
                }
                return Response({'status': status.HTTP_200_OK, 'msg': 'Cred Fetched', 'data': temp}, status=status.HTTP_200_OK)

            # data = Credential.objects.values(
            #     'id', 'user_name', 'active_tf', 'user_id', 'user_level_id')

            return Response({'status': status.HTTP_200_OK, 'msg': 'Creds Data Fetched', 'data': temp}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, formate=None):
        try:
            data = request.data
            serializer = serializers.CredentialAppSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'status': status.HTTP_200_OK, 'msg': 'Creds Data Saved', 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response({'status': status.HTTP_200_OK, 'msg': 'Creds Data Fetched', 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):

    def post(self, request, formate=None):

        try:
            username = request.data.get('user_name')
            password = request.data.get('password')

            user = Credential.objects.get(user_name=username)

            password_matches = check_password(password, user.password)

            if password_matches:
                token = get_tokens_for_user(user)
                return Response({'msg': 'Login Success', 'token': token}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Username or Password is not Valid'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"error ::: {e} <<")
            return Response({'msg': 'Username or Password is not Valid', 'error': 'Error Occured', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationView(APIView):

    def post(self, request, formate=None):
        serializer = serializers.UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            if user:
                json = serializer.data
                return Response({'msg': 'Registration Success', 'token': token, 'data': json}, status=status.HTTP_201_CREATED)
        return Response({'msg': 'Registration Failed', 'error': [serializer.errors], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
