from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from credApp.renderers import UserJSONRenderer
from projectApp.models import Project
from companyApp.models import Company
from . import serializers


class ProjectApiView(APIView):
    renderer_classes = [UserJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, formate=None):
        project_id = request.data.get('id')
        try:
            project = Project.objects.get(id=int(project_id))

            serializer = serializers.ProjectApiSerializer(
                project, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                project = serializer.data
                company_id = project.get('company')
                company = Company.objects.get(id=company_id)
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
        serializer = serializers.ProjectApiSerializer(
            data=request.data)
        if serializer.is_valid(raise_exception=True):
            project = serializer.save()
            if project:
                json = serializer.data
                return Response({'status': status.HTTP_201_CREATED, 'msg': 'Project Created',  'data': json},
                                status=status.HTTP_201_CREATED)

        return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error While adding Project', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
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


class ProjectListApiView(APIView):
    renderer_classes = [UserJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, formate=None):
        try:
            user = request.user
            print('uesr >>>> ', user.user_level_id)
            data = Project.objects.values(
                'id', 'name', 'company', 'description', 'is_active')
            temp = []

            for i, obj in enumerate(data):

                if (user.user_level_id == 1 or user.user_level_id == 2):
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
                        if(obj['is_active'] == True):
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
            projectList.sort(key=lambda temp: -temp['id'])
            return Response({'status': status.HTTP_200_OK, 'msg': 'Project Data Fetched', 'data': projectList}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)
