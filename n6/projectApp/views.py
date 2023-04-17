import json

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from credApp.renderers import UserJSONRenderer
from projectApp.models import Project
from companyApp.models import Company
from . import serializers
from userProjectAccessApp import serializers as userProjectAccessSerializers 


class ProjectApiView(APIView):
    renderer_classes = [UserJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, formate=None):
        """
        It takes a request, and returns a response

        :param request: The incoming request object
        :param formate: This is the format of the response
        :return: A list of all the projects in the database.
        """
        project_id = request.data.get('id')
        try:
            project = Project.objects.get(id=int(project_id))

            serializer = serializers.ProjectApiSerializer(
                project, data=request.data)
            if serializer.is_valid(raise_exception=True):
                
                project = serializer.data
                company_id = project.get('company')
                company = Company.objects.get(id=company_id)
                # company.projects.all()
                data = {
                    **project,
                    'company': {
                        'id': company.id,
                        'name': company.name,
                        'email_address': company.email_address,
                        'mobile_num': company.mobile_num,
                    }
                }
                return Response({'status': status.HTTP_200_OK, 'msg': 'Project Data Fetched', 'data': data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Project Not Found'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, formate=None):
        """
        If the serializer is valid, save the serializer and return a response with the serializer data

        :param request: The request object
        :param formate: This is the format of the response
        :return: The response is being returned in the form of a dictionary.
        """
        serializer = serializers.ProjectApiSerializer(
            data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            project = serializer.save()
            try:
                body = {
                    'user': request.user.id,
                    'project': project.id,
                }
                print(f"body ::: {body}")
                request.data.update(body)
                userProjectAccess = userProjectAccessSerializers.UserProjectAccessSerializer(data=request.data)
                if userProjectAccess.is_valid(raise_exception=True):
                    userProjectAccess.save()
            except Exception as e:
                raise e
            if project:
                json = serializer.data
                return Response({'status': status.HTTP_201_CREATED, 'msg': 'Project Created',  'data': json},
                                status=status.HTTP_201_CREATED)

        return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error While adding Project', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        """
        It takes the project id from the request data, checks if the project exists, if it does, it updates
        the project with the new data, if it doesn't, it returns a 404 error

        :param request: The request object
        :param format: The format of the response
        :return: The project data is being returned.
        """
        project_id = request.data.get('id')
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'msg': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.ProjectApiSerializer(
            project, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            project = serializer.data
            return Response({'status': status.HTTP_200_OK, 'msg': 'Project Data Updated', 'data': project}, status=status.HTTP_200_OK)
        return Response({'status': status.HTTP_404_NOT_FOUND, 'msg': 'Error Occured', 'error': serializer.errors}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, formate=None):
        """
        It takes a request object, and returns a response object

        :param request: The request object is the first parameter to any view. It contains the HTTP request
        that was made to the server
        :param formate: This is the format of the response
        :return: The response is being returned in the form of a dictionary.
        """
        try:
            project_id = request.data.get('id')

            project = Project.objects.get(id=project_id)
            project.is_active = request.data.get('is_active')
            project.save()
            return Response({'status': status.HTTP_200_OK, 'msg': 'Project Status Updated'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)


class ProjectListApiView(APIView):
    renderer_classes = [UserJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, formate=None):
        """
        If the user is a superuser or a company admin, then get all the projects and their company
        details. If the user is a company admin, then get only the active projects

        :param request: The request object
        :param formate: This is the format of the response
        :return: The data is being returned in the form of a list of dictionaries.
        """
        try:
            user = request.user
            print('uesr >>>> ', user.user_level_id)
            data = Project.objects.values(
                'id', 'name', 'company', 'description', 'is_active', 'user_id')
            temp = []

            for i, obj in enumerate(data):
                print('obj >>>> ', obj)
                print('user.id >>>> ', user.id)
                print(user.id == obj['user_id'])
                if (user.user_level_id != 1):
                    if (user.id == obj['user_id']):
                        company_id = Project.objects.values(
                            'company_id')[i]['company_id']
                        company = Company.objects.get(id=company_id)
                        if (user.user_level_id == 1):
                            temp.append(
                                {
                                    **obj,
                                    'company': {
                                        'id': company.id,
                                        'name': company.name,
                                        'email_address': company.email_address,
                                        'mobile_num': company.mobile_num,
                                    }
                                })
                        elif (user.user_level_id == 2):
                            if (obj['is_active'] == True):
                                temp.append(
                                    {
                                        **obj,
                                        'company': {
                                            'id': company.id,
                                            'name': company.name,
                                            'email_address': company.email_address,
                                            'mobile_num': company.mobile_num,
                                        }
                                    })
                else:
                    company_id = Project.objects.values(
                        'company_id')[i]['company_id']
                    company = Company.objects.get(id=company_id)
                    if (user.user_level_id == 1):
                        temp.append(
                            {
                                **obj,
                                'company': {
                                    'id': company.id,
                                    'name': company.name,
                                    'email_address': company.email_address,
                                    'mobile_num': company.mobile_num,
                                }
                            })
                    elif (user.user_level_id == 2):
                        if (obj['is_active'] == True):
                            temp.append(
                                {
                                    **obj,
                                    'company': {
                                        'id': company.id,
                                        'name': company.name,
                                        'email_address': company.email_address,
                                        'mobile_num': company.mobile_num,
                                    }
                                })

            projectList = list(temp)
            projectList.sort(
                key=lambda temp: (-temp['is_active'], -temp['id']))

            return Response({'status': status.HTTP_200_OK, 'msg': 'Project Data Fetched', 'data': projectList}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)
