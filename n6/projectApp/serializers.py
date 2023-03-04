from rest_framework import serializers
from projectApp.models import Project


class ProjectApiSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('company', 'name', 'description', 'is_active')

    def create(self, validated_data):

        project = {}
        project['name'] = validated_data.get('name')
        project['company'] = validated_data.get('company')
        project['description'] = validated_data.get('description')

        if (project['name'] is None):
            raise serializers.ValidationError(
                {'error': 'Project must have a name', 'status': 400})
        if (project['company'] is None):
            raise serializers.ValidationError(
                {'error': 'Project must have a valid Company', 'status': 400})

        data = Project(**project)
        data.save()

        return data

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.company = validated_data.get(
            'company', instance.company)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)

        instance.save()
        return instance
