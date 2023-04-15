from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from . import serializers
from rest_framework import permissions
from userApp.models import User, UserRole
from companyApp.models import Company
from credApp.renderers import UserJSONRenderer


class UserApiView(APIView):
    renderer_classes = [UserJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, formate=None):
        """
        It fetches a user from the database, and then updates the user with the data provided in the
        request
        
        :param request: The request object
        :param formate: This is the format of the response
        :return: A list of all the users in the database.
        """
        try:
            user_id = request.data.get('id')
            user = User.objects.get(id=int(user_id))
            serializer = serializers.UserRegistrationSerializer(
                user, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                company = Company.objects.get(
                    id=int(serializer.data['company']))
                user = serializer.data
                data = {
                    **user,
                    'company': {
                        'name': company.name,
                        'email_address': company.email_address,
                        'mobile_num': company.mobile_num,
                    }
                }
                return Response({'status': status.HTTP_200_OK, 'msg': 'User Fetched', 'data': data}, status=status.HTTP_200_OK)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error While getting user'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"error ::>: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Please Provide Valid User Id'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, formate=None):
        """
        If the company exists, create a user
        
        :param request: The request object
        :param formate: This is the format of the data that is being sent to the API
        :return: The response is a JSON object with the following keys:
        status: The HTTP status code of the response.
        msg: A message describing the status of the response.
        data: The data returned by the API.
        """
        company_id = request.data.get('company')

        try:
            Company.objects.get(id=int(company_id))
        except Company.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'msg': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserRegistrationSerializer(
            data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                json = serializer.data
                return Response({'status': status.HTTP_201_CREATED, 'msg': 'User Created',  'data': json},
                                status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        """
        It gets the user object using the user ID, and then updates the user object with the data provided
        in the request
        
        :param request: The request object contains all the information about the request that was made to
        the server
        :param format: This is the format of the response. It can be either JSON or XML
        :return: The response is being returned in the form of a dictionary.
        """
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


class UserListApiView(APIView):
    renderer_classes = [UserJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, formate=None):
        """
        It fetches all the users from the database and returns the data in the form of a list.
        
        :param request: The initial request object sent from the client
        :param formate: This is the format of the response
        :return: A list of dictionaries.
        """
        try:
            data = User.objects.values(
                'id', 'first_name', 'last_name', 'email_address', 'mobile_num', 'company_id')
            temp = []
            for i, obj in enumerate(data):
                company_id = User.objects.values('company_id')[i]['company_id']
                company = Company.objects.get(id=company_id)
                temp.append(
                    {
                        **obj,
                        'company': {
                            'name': company.name,
                            'email_address': company.email_address,
                            'mobile_num': company.mobile_num,
                        }
                    })

            userList = list(temp)
            userList.sort(key=lambda temp: -temp['id'])

            return Response({'status': status.HTTP_200_OK, 'msg': 'User Data Fetched', 'data': userList}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)


class UserRoleListApiView(APIView):
    renderer_classes = [UserJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, formate=None):
        """
        It fetches all the user roles from the database and returns them in a list
        
        :param request: The incoming request
        :param formate: This is the format of the response. It can be either JSON or XML
        :return: A list of dictionaries.
        """
        try:
            data = UserRole.objects.values(
                'id', 'role')
            userRoleList = list(data)
            userRoleList.sort(key=lambda data: data['id'])

            return Response({'status': status.HTTP_200_OK, 'msg': 'User Roles Data Fetched', 'data': userRoleList}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)
