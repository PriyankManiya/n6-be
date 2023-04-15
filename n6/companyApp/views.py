from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from credApp.renderers import UserJSONRenderer
from companyApp.models import Company
from . import serializers


class CompanyApiView(APIView):
    renderer_classes = [UserJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, formate=None):
        """
        If the company exists, then update the company's data with the data provided in the request
        
        :param request: The incoming request
        :param formate: This is the format of the response
        """
        company_id = request.data.get('id')
        try:
            company = Company.objects.get(id=int(company_id))
            
            serializer = serializers.CompanyRegistrationSerializer(
            company, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'status': status.HTTP_200_OK, 'msg': 'Company Data Fetched', 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Company Not Found'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, formate=None):
        """
        It takes a request, validates the request, saves the request, and returns a response
        
        :param request: The request object
        :param formate: This is the format of the response
        :return: The response is being returned in the form of a JSON object.
        """
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
        """
        It takes a company id, finds the company, and updates the company's data with the data in the
        request
        
        :param request: The request object
        :param format: The format of the response
        :return: The serializer.data is being returned.
        """
        company_id = request.data.get('id')
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'msg': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.CompanyRegistrationSerializer(
            company, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'status': status.HTTP_200_OK, 'msg': 'Company Data Updated', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyListApiView(APIView):
    renderer_classes = [UserJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, formate=None):
        """
        This function is used to fetch all the companies from the database.
        
        :param request: The incoming request
        :param formate: This is the format of the response. It can be either JSON or XML
        :return: A list of dictionaries.
        """
        try:
            data = Company.objects.values(
                'id', 'name', 'email_address', 'mobile_num', 'is_active')
            companyList = list(data)
            companyList.sort(key=lambda data: ( -data['is_active'], -data['id']))
            return Response({'status': status.HTTP_200_OK, 'msg': 'Company Data Fetched', 'data': companyList}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)