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
from noteApp.models import Note
from attachmentApp.models import Attachment
from credApp.renderers import UserJSONRenderer
from userProjectAccessApp.models import UserProjectAccess

from json import JSONEncoder


class NoteListApiView(APIView):
    renderer_classes = [UserJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id, formate=None):
        """
        It fetches all the notes from the database and returns them in a list
        
        :param request: The request object
        :param id: The id of the project
        :param formate: This is the format of the response
        :return: A list of notes that are associated with a project.
        """
        try:
            proj_id = id
            requestUser = request.user
            # if (Credential.has_perm(user, 'is_admin') == False):
            #     return Response({'status': status.HTTP_401_UNAUTHORIZED, 'msg': 'Sorry You Do not have enough permissions'}, status=status.HTTP_401_UNAUTHORIZED)

            note = Note.objects.values(
                'id', 'user', 'project', 'user', 'responded_note', 'topic', 'content_html', 'read_tf', 'is_active', 'created_at', 'updated_at')
            temp = []
            for i, obj in enumerate(note):
                user_id = Note.objects.values('user')[
                    i]['user']
                project_id = Note.objects.values('project')[
                    i]['project']
                user = User.objects.get(id=user_id)

                attachmentList = []

                attachment = Attachment.objects.filter(
                    note_id=obj.get('id')).values('id', 'note_id', 'filename', 'path', 'is_active', 'created_at', 'updated_at')

                attachmentList = [
                    {
                        'id': f.get('id'),
                        'note_id': f.get('note_id'),
                        'filename': f.get('filename'),
                        'path': f.get('path'),
                        'is_active': f.get('is_active'),
                        'created_at': f"{f.get('created_at')}",
                        'updated_at': f"{f.get('updated_at')}"
                    } for f in attachment]

                # if (attachment is not None or attachment != '' or attachment != []) : attachmentList.append(attachment)

                project = Project.objects.get(id=project_id)
                note_updated_at = obj.get('updated_at')
                note_created_at = obj.get('created_at')
                obj.pop('created_at')
                obj.pop('updated_at')

                if (Credential.has_perm(requestUser, 'is_admin') == False):
                    if (str(proj_id) == str(project_id) and obj.get('is_active') == True):
                        if (obj.get('responded_note') == 0 or obj.get('responded_note') is None):
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
                                    'attachments': attachmentList,
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
                                    'updated_at': f"{note_updated_at}",
                                    'created_at': f"{note_created_at}",
                                })
                else:
                    if (str(proj_id) == str(project_id)):
                        if (obj.get('responded_note') == 0 or obj.get('responded_note') is None):
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
                                    'updated_at': f"{note_updated_at}",
                                    'created_at': f"{note_created_at}",
                                })

            noteList = list(temp)
            noteList.sort(key=lambda temp: -temp['id'])

            return Response({'status': status.HTTP_200_OK, 'msg': 'Note Data Fetched', 'data': noteList}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)


class RespondNoteApiView(APIView):
    renderer_classes = [UserJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, formate=None):
        """
        It fetches the original note and all the responded notes of the original note
        
        :param request: The request object passed in to a view by the framework
        :param formate: This is the format of the response
        :return: A list of notes that are responded to the original note.
        """
        try:
            note_id = int(request.data.get('note_id'))
            user = request.user
            note = Note.objects.values(
                'id', 'user', 'project', 'responded_note', 'topic', 'content_html', 'read_tf', 'is_active', 'created_at', 'updated_at')
            temp = []
            original_note = Note.objects.get(id=note_id)
            original_note_user = User.objects.get(id=original_note.user.pk)
            for i, obj in enumerate(note):
                user_id = Note.objects.values('user')[
                    i]['user']
                project_id = Note.objects.values('project')[
                    i]['project']
                user = User.objects.get(id=user_id)
                project = Project.objects.get(id=project_id)
                note_updated_at = obj.get('updated_at')
                note_created_at = obj.get('created_at')
                obj.pop('created_at')
                obj.pop('updated_at')

                if (obj.get('responded_note') == note_id):
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
                            'updated_at': f"{note_updated_at}",
                            'created_at': f"{note_created_at}",
                        })

            respondedNoteList = list(temp)
            respondedNoteList.sort(key=lambda temp: -temp['id'])

            json = {
                'original_note': {
                    "topic": original_note.topic,
                    "content_html": original_note.content_html,
                    "read_tf": original_note.read_tf,
                    "is_active": original_note.is_active,
                    "updated_at": f"{original_note.updated_at}",
                    "created_at": f"{original_note.created_at}",
                    'user': {
                        'first_name': original_note_user.first_name,
                        'last_name': original_note_user.last_name,
                        'email_address': original_note_user.email_address,
                        'mobile_num': original_note_user.mobile_num,
                        'is_active': original_note_user.is_active,
                        'company_id': original_note_user.company.pk,
                        'company': {
                            'name': original_note_user.company.name,
                            'email_address': original_note_user.company.email_address,
                            'mobile_num': original_note_user.company.mobile_num,
                            'is_active': original_note_user.company.is_active,
                        }}
                },
                'responded_note':
                    respondedNoteList

            }

            return Response({'status': status.HTTP_200_OK, 'msg': 'Responded Note Data Fetched', 'data': json}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, formate=None):
        """
        It takes a request, validates it, saves it, and returns a response
        
        :param request: The request object
        :param formate: This is the format of the response
        :return: The response is being returned in the form of a dictionary.
        """
        serializer = serializers.RespondNoteApiSerializer(
            data=request.data)
        if serializer.is_valid(raise_exception=True):
            attachment = serializer.save()
            if attachment:
                data = serializer.data
                temp = {
                    **data,
                }
                return Response({'status': status.HTTP_201_CREATED, 'msg': 'Note Responded',  'data': temp},
                                status=status.HTTP_201_CREATED)

        return Response({'status': status.HTTP_400_BAD_REQUEST, 'errors': serializer.errors, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)


class NoteApiView(APIView):
    renderer_classes = [UserJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, formate=None):
        """
        It takes a request, serializes it, checks if it's valid, saves it, and returns a response
        
        :param request: The request object
        :param formate: This is the format of the response
        :return: The response is being returned in the form of a dictionary.
        """
        serializer = serializers.NoteApiSerializer(
            data=request.data)
        if serializer.is_valid(raise_exception=True):
            attachment = serializer.save()
            if attachment:
                data = serializer.data
                temp = {
                    **data,
                }
                return Response({'status': status.HTTP_201_CREATED, 'msg': 'Note Responded',  'data': temp},
                                status=status.HTTP_201_CREATED)

        return Response({'status': status.HTTP_400_BAD_REQUEST, 'errors': serializer.errors, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, formate=None):
        """
        It takes the id of the note from the request, finds the note with that id, sets the is_active field
        to False and saves the note
        
        :param request: The request object is used to access the request data
        :param formate: This is the format of the response
        :return: The response is being returned.
        """
        try:
            note_id = int(request.data.get('id'))

            note = Note.objects.get(id=note_id)
            note.is_active = False
            note.save()
            return Response({'status': status.HTTP_200_OK, 'msg': 'Note Disabled'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, formate=None):
        """
        It takes the note id from the request data, fetches the note from the database, sets the is_active
        field to True and saves the note
        
        :param request: The request object is used to get the request data
        :param formate: This is the format of the response
        :return: The response is being returned in the form of a dictionary.
        """
        try:
            note_id = int(request.data.get('id'))
            note = Note.objects.get(id=note_id)
            note.is_active = True
            note.save()
            return Response({'status': status.HTTP_200_OK, 'msg': 'Note Enabled'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)


class NoteReadApiView(APIView):
    renderer_classes = [UserJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, formate=None):
        """
        It takes the note id from the request, finds the note with that id, sets the read_tf field to True,
        and saves the note
        
        :param request: The request object is the first parameter to the view. It contains the request data,
        such as the HTTP method, the URL, the headers, and the body
        :param formate: This is the format of the response
        :return: A list of all the notes that are unread.
        """
        try:
            note_id = int(request.data.get('id'))
            note = Note.objects.get(id=note_id)
            note.read_tf = True
            note.save()
            return Response({'status': status.HTTP_200_OK, 'msg': 'Note Read'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"error ::: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)
