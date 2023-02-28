from rest_framework import serializers
from .models import Credential, User

from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# example
class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email_address', 'mobile_num','company')

    def create(self, validated_data):
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

