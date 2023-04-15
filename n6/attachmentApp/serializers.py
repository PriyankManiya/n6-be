from rest_framework import serializers
from .models import Attachment


class AttachmentApiSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attachment
        fields = ('id','note', 'filename', 'path', 'created_at', 'updated_at', 'created_at')

    def create(self, validated_data):
        """
        If the data is valid, create a new Attachment object and save it to the database
        
        :param validated_data: The data that has been validated by the serializer
        :return: The data that was saved to the database.
        """

        attachment = {}
        attachment['note'] = validated_data.get('note')
        attachment['filename'] = validated_data.get('filename')
        attachment['path'] = validated_data.get('path')

        if (attachment['note'] is None):
            raise serializers.ValidationError(
                {'error': 'Attachment must have a note id', 'status': 400})
        if (attachment['filename'] is None):
            raise serializers.ValidationError(
                {'error': 'Attachment must have a valid filename', 'status': 400})
        if (attachment['path'] is None):
            raise serializers.ValidationError(
                {'error': 'Attachment must have a valid path', 'status': 400})

        data = Attachment(**attachment)
        data.save()

        return data