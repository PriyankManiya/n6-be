from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from credApp.renderers import UserJSONRenderer
from . import serializers


class AttachmentApiView(APIView):
    renderer_classes = [UserJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, formate=None):
        serializer = serializers.AttachmentApiSerializer(
            data=request.data)
        if serializer.is_valid(raise_exception=True):
            attachment = serializer.save()
            if attachment:
                data = serializer.data
                temp = {
                    **data, 'note_id': data.get('note')
                }
                temp.pop('note')
                return Response({'status': status.HTTP_201_CREATED, 'msg': 'Attachment Created',  'data': temp},
                                status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
