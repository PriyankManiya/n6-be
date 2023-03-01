from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from credApp.models import Credential
from credApp.serializers import CredentialAppSerializer

# Create your views here.


class CredListApiView(APIView):

    def get(self, request, formate=None):
        try:
            data = Credential.objects.values(
                'id', 'user_name', 'active_tf', 'user_id', 'user_level_id')
            credList = list(data)
            return Response({'status': status.HTTP_200_OK, 'msg': 'Creds Data Fetched', 'data': credList}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)

    


class CredApiView(APIView):

    def get(self, request, formate=None):
        try:
            data = Credential.objects.values(
                'id', 'user_name', 'active_tf', 'user_id', 'user_level_id')
            return Response({'status': status.HTTP_200_OK, 'msg': 'Creds Data Fetched', 'data': data[0]}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, formate=None):
        try:
            data = request.data
            print(f"data ::: {data}")
            serializer = CredentialAppSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'status': status.HTTP_200_OK, 'msg': 'Creds Data Saved', 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response({'status': status.HTTP_200_OK, 'msg': 'Creds Data Fetched', 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)