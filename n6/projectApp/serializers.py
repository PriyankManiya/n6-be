from rest_framework import serializers
from projectApp.models import Project


class ProjectApiSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id','company', 'name', 'description', 'is_active')

    def create(self, validated_data):
        """
        If the project name is not None, and the company is not None, then create a new project with the
        given name and company
        
        :param validated_data: The data that has been validated by the serializer
        :return: The data that was saved to the database.
        """

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
        """
        The update function takes in an instance of the model, and a validated_data dictionary. 
        It then updates the instance with the validated_data, and returns the instance
        
        :param instance: The instance of the model that is being updated
        :param validated_data: The data that was validated by the serializer
        :return: The instance is being returned.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.company = validated_data.get(
            'company', instance.company)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)

        instance.save()
        return instance
