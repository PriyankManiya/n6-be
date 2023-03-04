from rest_framework import serializers
from noteApp.models import Note


class RespondNoteApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'project', 'user', 'topic', 'content_html', 'responded_note',
                  'read_tf', 'is_active', 'updated_at', 'created_at')

    def create(self, validated_data):

        note = {}
        note['project'] = validated_data.get('project')
        note['user'] = validated_data.get('user')
        note['responded_note'] = validated_data.get('responded_note')
        note['topic'] = validated_data.get('topic')
        note['content_html'] = validated_data.get('content_html')

        if (note['project'] is None):
            raise serializers.ValidationError(
                {'error': 'Note must have a project id', 'status': 400})
        if (note['user'] is None):
            raise serializers.ValidationError(
                {'error': 'Note must have a valid user id', 'status': 400})
        if (note['responded_note'] is None):
            raise serializers.ValidationError(
                {'error': 'Note must have a valid responded_note id', 'status': 400})
        if (note['topic'] is None):
            raise serializers.ValidationError(
                {'error': 'Note must have a valid topic', 'status': 400})
        if (note['content_html'] is None):
            raise serializers.ValidationError(
                {'error': 'Note must have a valid content_html', 'status': 400})

        data = Note(**note)
        data.save()

        return data

class NoteApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'project', 'user', 'topic', 'content_html', 'responded_note',
                  'read_tf', 'is_active', 'updated_at', 'created_at')

    def create(self, validated_data):

        note = {}
        note['project'] = validated_data.get('project')
        note['user'] = validated_data.get('user')
        note['topic'] = validated_data.get('topic')
        note['content_html'] = validated_data.get('content_html')

        if (note['project'] is None):
            raise serializers.ValidationError(
                {'error': 'Note must have a project id', 'status': 400})
        if (note['user'] is None):
            raise serializers.ValidationError(
                {'error': 'Note must have a valid user id', 'status': 400})
        if (note['topic'] is None):
            raise serializers.ValidationError(
                {'error': 'Note must have a valid topic', 'status': 400})
        if (note['content_html'] is None):
            raise serializers.ValidationError(
                {'error': 'Note must have a valid content_html', 'status': 400})

        data = Note(**note)
        data.save()

        return data