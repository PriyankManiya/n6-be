from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from credApp.models import Credential
from . import serializers
from userApp.models import UserRole, User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from rest_framework import permissions
from credApp.renderers import UserJSONRenderer
from django.contrib.auth import authenticate


def get_tokens_for_user(user):
    """
    It creates a new refresh token for the user, and returns the refresh token and the access token
    associated with it
    
    :param user: The user object that you want to generate tokens for
    :return: A dictionary with two keys: refresh_token and access_token.
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }


# This class is used to fetch all the credentials of the users
class CredListApiView(APIView):
    renderer_classes = [UserJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, formate=None):
        """
        I want to get all the data from the Credential table, and then for each row, I want to get the
        user_level_id and user_id, and then get the corresponding UserRole and User objects, and then
        add the user_level_id and user_id to the temp list, and then return the temp list
        
        :param request: The request object
        :param formate: This is the format of the response
        :return: A list of dictionaries.
        """
        try:
            loggedInUser = request.user
            data = Credential.objects.values(
                'id', 'user_name', 'user_id', 'user_level_id', 'is_active')
            temp = []
            if loggedInUser.user_level_id == 1:
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
            else:
                return Response({'status': status.HTTP_401_UNAUTHORIZED, 'msg': 'Sory You do not have enough Permissions'}, status=status.HTTP_401_UNAUTHORIZED)

            credList = list(temp)
            credList.sort(key=lambda temp: -temp['id'])
            return Response({'status': status.HTTP_200_OK, 'msg': 'Creds Data Fetched', 'data': credList}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)


# It's a view that allows you to get, post and put data to the Credential model
class CredApiView(APIView):
    renderer_classes = [UserJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, formate=None):
        """
        I'm trying to get the user's data from the User model and the user's role from the UserRole
        model and then merge them into one object
        
        :param request: The request object passed to the view
        :param formate: This is the format of the response
        :return: The user's credentials are being returned.
        """
        try:
            user = request.user
            serializer = serializers.CredProfileSerializer(user)
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
                        'id': user.company.id,
                        'name': user.company.name,
                        'email_address': user.company.email_address,
                        'mobile_num': user.company.mobile_num,
                    }
                }
            }

            return Response({'status': status.HTTP_200_OK, 'msg': 'Creds Data Fetched', 'data': temp}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, formate=None):
        """
        It takes a request, validates the data, saves the data, and returns a response
        
        :param request: The request object
        :param formate: This is the format of the response. It can be either JSON or XML
        :return: The response is being returned in the form of a dictionary.
        """
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

    def put(self, request, format=None):
        """
        It takes the id of the credential from the request data, checks if the credential exists, if it
        does, it updates the credential with the data from the request
        
        :param request: The request object is the first parameter to the view. It contains the request
        data, including the request body, query parameters, and headers
        :param format: The format of the response
        :return: The serializer.data is being returned.
        """
        cred_id = request.data.get('id')
        try:
            credential = Credential.objects.get(id=cred_id)
        except Credential.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'msg': 'Credential not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.CredentialAppUpdateSerializer(
            credential, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'status': status.HTTP_200_OK, 'msg': 'Credential Data Updated', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# It takes the username and password from the request, checks if the username exists in the database,
# if it does, it checks if the password matches the one in the database, if it does, it returns a
# token, if it doesn't, it returns an error
class UserLoginView(APIView):

    def post(self, request, formate=None):
        """
        It takes the username and password from the request, checks if the username exists in the
        database, if it does, it checks if the password matches the one in the database, if it does, it
        returns a token, if it doesn't, it returns an error
        
        :param request: The request object
        :param formate: This is the format of the response
        :return: The response is a JSON object with the following keys:
        """

        try:
            username = request.data.get('username')
            password = request.data.get('password')

            try:
                user = Credential.objects.get(user_name=username)
            except Exception as e:
                return Response({'msg': 'Username or Password is not Valid', 'status': status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)

            password_matches = check_password(password, user.password)

            if password_matches:
                token = get_tokens_for_user(user)
                return Response({'msg': 'Login Success', **token, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Username or Password is not Valid', 'status': status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(f"error is ::: {e} <<")
            return Response({'msg': 'Something Went Wrong', 'error': 'Error Occured', 'status': status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)


# The UserRegistrationView class is a subclass of the APIView class. It has a post method that takes
# in a request object and a formate object. The post method creates a serializer object using the
# UserRegistrationSerializer class. The serializer object is then validated using the is_valid method.
# If the serializer object is valid, the user is saved and a token is generated for the user. If the
# user is saved, a json object is created using the data attribute of the serializer object. The json
# object is then returned as a response. If the serializer object is not valid, an error message is
# returned as a response
class UserRegistrationView(APIView):

    def post(self, request, formate=None):
        """
        It takes a request, validates the data, saves the data, and returns a response
        
        :param request: The request object
        :param formate: This is the format of the response
        :return: The response is being returned in the form of a dictionary.
        """
        serializer = serializers.UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            if user:
                json = serializer.data
                return Response({'msg': 'Registration Success', **token, 'data': json, 'status': status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
        return Response({'msg': 'Registration Failed', 'error': [serializer.errors], 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


# It takes the old password, checks if it's valid, and if it is, it changes the password
class UserChangePasswordView(APIView):
    renderer_classes = [UserJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, formate=None):
        """
        It takes the old password, checks if it's valid, then changes the password to the new one
        
        :param request: The request object
        :param formate: This is the format of the response
        :return: The response is being returned in the form of a dictionary.
        """

        userCred = {
            'password': request.data.get('old_password'),
            'user_name': request.user.user_name,
        }

        loginSerializer = serializers.CredLoginSerializer(data=userCred)

        if loginSerializer.is_valid(raise_exception=True):
            user_name = loginSerializer.data.get('user_name')
            password = loginSerializer.data.get('password')
            user = authenticate(**userCred)
            if user is not None:
                serializer = serializers.UserChangePasswordSerializer(
                    data=request.data, context={'user': user})
                serializer.is_valid(raise_exception=True)
                return Response({'msg': 'Password Changed Success', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Old Password is not Valid', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)


# It takes in a username, checks if the username is valid, and if it is, it sends a password reset
# link to the user's email
class SendEmailView(APIView):
    renderer_classes = [UserJSONRenderer]

    def post(self, request, formate=None):
        """
        If the serializer is valid, save the serializer and return a response with a message and the
        serializer data. If the serializer is not valid, return a response with an error message and the
        serializer errors
        
        :param request: The request object
        :param formate: This is the format of the data that is being sent to the API
        :return: The response is a JSON object with the following keys:
        """
        serializer = serializers.SendEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Password Reset Link has been sent', 'data': serializer.data, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        return Response({'msg': 'Please Provide Valid Username', 'error': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST, }, status=status.HTTP_400_BAD_REQUEST)


# It takes the request data, validates it, and if it's valid, it saves it
class ResetPasswordView(APIView):
    renderer_classes = [UserJSONRenderer]

    def post(self, request, cid, token, formate=None):
        """
        It takes the request data, validates it, and if it's valid, it saves it
        
        :param request: The request object
        :param cid: The id of the user who is requesting the password reset
        :param token: The token that was sent to the user's email
        :param formate: This is the format of the response. It can be either json or xml
        :return: The response is being returned.
        """
        serializer = serializers.ResetPasswordSerializer(
            data=request.data, context={'cid': cid, 'token': token})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Password Reset Success', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)
