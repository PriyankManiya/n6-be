import os
from datetime import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from credApp.renderers import UserJSONRenderer
from . import serializers
from attachmentApp.models import Attachment

class AttachmentApiView(APIView):
    renderer_classes = [UserJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'File not found'}, status=status.HTTP_400_BAD_REQUEST)

        fs = FileSystemStorage()
        filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}-{file.name}"
        saved_file = fs.save(os.path.join(
            settings.MEDIA_ROOT, 'attachment', filename), file)
        file_url = fs.url(saved_file)

        attachment_data = {
            'note': request.data.get('note'),
            'filename': file.name,
            'path': file_url,
        }

        serializer = serializers.AttachmentApiSerializer(data=attachment_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': status.HTTP_201_CREATED, 'msg': 'Attachment created', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, format=None):
        attachment_id = request.data.get('id')
        try:
            attachment = Attachment.objects.get(id=attachment_id)
        except Attachment.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'msg': 'Attachment not found'}, status=status.HTTP_404_NOT_FOUND)
        attachment.delete()
        return Response({'status': status.HTTP_200_OK, 'msg': 'Attachment deleted'}, status=status.HTTP_200_OK)
