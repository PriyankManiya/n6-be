from rest_framework import serializers
from .models import Company


class CompanyRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('id','name', 'email_address', 'mobile_num', 'is_active')

    def create(self, validated_data):
        """
        It updates the company data.
        
        :param validated_data: The data that has been validated by the serializer
        :return: The instance of the object being updated.
        """

        company = {}
        company['name'] = validated_data.get('name')
        company['email_address'] = validated_data.get('email_address')
        company['mobile_num'] = validated_data.get('mobile_num')
        company['is_active'] = validated_data.get('is_active')

        if (company['name'] is None):
            raise serializers.ValidationError(
                {'error': 'Company must have a name', 'status': 400})
        if (company['email_address'] is None):
            raise serializers.ValidationError(
                {'error': 'Company must have a valid email address', 'status': 400})
        if (company['mobile_num'] is None):
            company['mobile_num'] = 0
        if (company['is_active'] is None):
            company['is_active'] = True

        data = Company(**company)
        data.save()

        return data

    def update(self, instance, validated_data):
        """
        The update() function takes in the instance of the model that we want to update, and the
        validated_data that we want to update it with. 
        
        It then updates the instance with the validated_data, and returns the updated instance
        
        :param instance: The instance of the model that is being updated
        :param validated_data: The data that was validated by the serializer
        :return: The instance is being returned.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.email_address = validated_data.get(
            'email_address', instance.email_address)
        instance.mobile_num = validated_data.get(
            'mobile_num', instance.mobile_num)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance
