from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from . import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from .models import Company
import json
import jsonpickle
from json import JSONEncoder

# Create your views here.


class CompanyApiView(APIView):

    def get(self, request, formate=None):
        company_id = request.data.get('id')
        try:
            company = Company.objects.get(id=int(company_id))
            
            serializer = serializers.CompanyRegistrationSerializer(
            company, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'status': status.HTTP_200_OK, 'msg': 'Company Data Updated', 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Company Not Found'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, formate=None):
        serializer = serializers.CompanyRegistrationSerializer(
            data=request.data)
        if serializer.is_valid(raise_exception=True):
            company = serializer.save()
            if company:
                json = serializer.data
                return Response({'status': status.HTTP_201_CREATED, 'msg': 'Company Created',  'data': json},
                                status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        company_id = request.data.get('id')
        try:
            # get the company object using the company ID
            company = Company.objects.get(id=company_id)
            # replace `name` with the actual name field of your Company model
        except Company.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'msg': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.CompanyRegistrationSerializer(
            company, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'status': status.HTTP_200_OK, 'msg': 'Company Data Updated', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyListApiView(APIView):

    def get(self, request, formate=None):
        try:
            data = Company.objects.values(
                'id', 'name', 'email_address', 'mobile_num')
            companyList = list(data)
            return Response({'status': status.HTTP_200_OK, 'msg': 'Company Data Fetched', 'data': companyList}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)