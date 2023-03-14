from rest_framework import serializers
from userApp.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'email_address', 'mobile_num','company')

    def create(self, validated_data):
        """
        The function takes in a validated_data dictionary, creates a new user dictionary, and then saves
        the new user to the database
        
        :param validated_data: The validated data from the serializer
        :return: The data that is being returned is the data that is being saved to the database.
        """
        print(f"validated_data ::: {validated_data}")
        user = {}
        user['first_name'] = validated_data.get('first_name')
        user['last_name'] = validated_data.get('last_name')
        user['email_address'] = validated_data.get('email_address')
        user['mobile_num'] = validated_data.get('mobile_num')
        user['company'] = validated_data.get('company')

        if (user['first_name'] is None):
            raise serializers.ValidationError(
                {'error': 'User must have a First Name', 'status': 400})
        if (user['email_address'] is None):
            raise serializers.ValidationError(
                {'error': 'User must have a valid email address', 'status': 400})
            
        print(f"user >>> company ::: {user['company']}")
        if (user['company'] is None):
            raise serializers.ValidationError(
                {'error': 'Please provide a valid Company Id', 'status': 400})

        if (user['last_name'] is None):
            user['last_name'] = ''

        if (user['mobile_num'] is None):
            user['mobile_num'] = 0

        data = User(**user)
        data.save()

        return data

    def update(self, instance, validated_data):
        """
        The update() function is called when a PUT request is made to the API. 
        
        The function takes in the instance of the object to be updated, and the validated_data dictionary. 
        
        The validated_data dictionary contains the data that was passed in the request. 
        
        The function then updates the instance with the validated_data and returns the instance
        
        :param instance: The current instance of the object being updated
        :param validated_data: The data that was validated by the serializer
        :return: The instance is being returned.
        """
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.email_address = validated_data.get(
            'email_address', instance.email_address)
        instance.mobile_num = validated_data.get(
            'mobile_num', instance.mobile_num)
        instance.save()
        return instance

