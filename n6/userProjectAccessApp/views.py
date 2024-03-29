from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from . import serializers
from rest_framework import permissions
from userApp.models import User
from projectApp.models import Project
from credApp.models import Credential
from credApp.renderers import UserJSONRenderer
from userProjectAccessApp.models import UserProjectAccess


class UserProjectAccessListApiView(APIView):
    renderer_classes = [UserJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, formate=None):
        """
        It fetches all the data from the UserProjectAccess table and then fetches the data from the User
        and Project tables and then combines all the data into a single list and then returns the list
        
        :param request: The request object
        :param formate: This is the format of the response
        :return: A list of all the UserProjectAccess objects in the database.
        """
        try:
            user = request.user
            print(f"user.user_level_id ::: {user.user_level_id}")
            if (int(user.user_level_id) == 4):
                return Response({'status': status.HTTP_401_UNAUTHORIZED, 'msg': 'Sorry You Do not have enough permissions'}, status=status.HTTP_401_UNAUTHORIZED)
            data = UserProjectAccess.objects.values(
                'id', 'user', 'project_id', 'access_url', 'is_active').filter(user_id=user.user_id)

            temp = []
            for i, obj in enumerate(data):
                user_id = UserProjectAccess.objects.values('user')[
                    i]['user']
                project_id = obj['project_id']
                user = User.objects.get(id=user_id)
                project = Project.objects.get(id=project_id)
                temp.append(
                    {
                        **obj,
                        'user': {
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'email_address': user.email_address,
                            'mobile_num': user.mobile_num,
                            'is_active': user.is_active,
                            'company_id': user.company.pk,
                            'company': {
                                'name': user.company.name,
                                'email_address': user.company.email_address,
                                'mobile_num': user.company.mobile_num,
                                'is_active': user.company.is_active,
                            }
                        },
                        'project': {
                            'id': project.pk,
                            'name': project.name,
                            'description': project.description,
                            'is_active': project.is_active,
                            'company': {
                                'name': project.company.name,
                                'email_address': project.company.email_address,
                                'mobile_num': project.company.mobile_num,
                                'is_active': project.company.is_active,
                            }
                        }
                    })

            userProjectAccessList = list(temp)
            userProjectAccessList.sort(key=lambda temp: (-temp['is_active'], -temp['id']))

            return Response({'status': status.HTTP_200_OK, 'msg': 'User ProjectAccess Data Fetched', 'data': userProjectAccessList}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)


class UserProjectAccessApiView(APIView):
    renderer_classes = [UserJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, formate=None):
        """
        It fetches the user project access data based on the id passed in the request
        
        :param request: The request object passed in to the view
        :param formate: This is the format of the response
        :return: A list of all the user project accesses
        """
        loggedInUser = request.user
        user_project_access_id = request.data.get('id')
        try:
            userProjectAccess = UserProjectAccess.objects.get(
                id=int(user_project_access_id))
            user_id = userProjectAccess.user.pk
            project_id = userProjectAccess.project.pk
            user = User.objects.get(id=user_id)
            project = Project.objects.get(id=project_id)

            if (Credential.has_perm(loggedInUser, 'is_admin') == False):
                if loggedInUser.id != user.id:
                    return Response({'status': status.HTTP_401_UNAUTHORIZED, 'msg': 'You do not have access to this project'}, status=status.HTTP_401_UNAUTHORIZED)
                if userProjectAccess.is_active == False:
                    return Response({'status': status.HTTP_401_UNAUTHORIZED, 'msg': 'Project is not active'}, status=status.HTTP_401_UNAUTHORIZED)

            temp = {
                'id': userProjectAccess.id,
                'is_active': userProjectAccess.is_active,
                'access_url': userProjectAccess.access_url,
                'otp': userProjectAccess.otp,

                'user': {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email_address': user.email_address,
                    'mobile_num': user.mobile_num,
                    'is_active': user.is_active,
                    'company_id': user.company.pk,
                    'company': {
                        'name': user.company.name,
                        'email_address': user.company.email_address,
                        'mobile_num': user.company.mobile_num,
                        'is_active': user.company.is_active,
                    }
                },
                'project': {
                    'name': project.name,
                    'description': project.description,
                    'is_active': project.is_active,
                    'company': {
                        'name': project.company.name,
                        'email_address': project.company.email_address,
                        'mobile_num': project.company.mobile_num,
                        'is_active': project.company.is_active,
                    }
                },
                'otp_updated_at': f"{userProjectAccess.otp_updated_at}",
                'access_url_updated_at': f"{userProjectAccess.access_url_updated_at}",
                'updated_at': f"{userProjectAccess.updated_at}",
                'created_at': f"{userProjectAccess.created_at}",
            }

            userProjectAccessList = temp
            return Response({'status': status.HTTP_200_OK, 'msg': 'User Project Access Data Fetched', 'data': userProjectAccessList}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'User Project Access Not Found'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, formate=None):
        """
        It takes a request, validates the data, saves the data, and returns a response
        
        :param request: The request object
        :param formate: This is the format of the response
        """
        serializer = serializers.UserProjectAccessSerializer(
            data=request.data)
        if serializer.is_valid(raise_exception=True):
            userProjectAccess = serializer.save()
            if userProjectAccess:
                json = serializer.data
                return Response({'status': status.HTTP_201_CREATED, 'msg': 'User Project Access Created',  'data': json},
                                status=status.HTTP_201_CREATED)

        return Response({'error': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occurend in User Project Access'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        """
        It updates the user project access data.
        
        :param request: The request object passed in from the view
        :param format: The format of the response
        :return: The serializer.data is being returned.
        """
        user_project_access_id = request.data.get('id')
        try:
            userProjectAccess = UserProjectAccess.objects.get(
                id=user_project_access_id)
        except UserProjectAccess.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'msg': 'User Project Access not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.UserProjectAccessSerializer(
            userProjectAccess, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'status': status.HTTP_200_OK, 'msg': 'User Project Access Data Updated', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
