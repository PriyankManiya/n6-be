from rest_framework import serializers
from userProjectAccessApp.models import UserProjectAccess

from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# example
class GetUserProjectAccessSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProjectAccess
        fields = ('id', 'user_id', 'project_id',
                  'is_active', 'access_url', 'otp')


class UserProjectAccessSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProjectAccess
        fields = ('user_id', 'project_id', 'access_url', 'otp')

    def create(self, validated_data):
        userProjectAccess = {}
        userProjectAccess['user_id'] = validated_data.get('user_id')
        userProjectAccess['project_id'] = validated_data.get('project_id')

        print(
            f"userProjectAccess['project_id'] ::: {userProjectAccess['project_id']}")
        print(
            f"userProjectAccess['user_id'] ::: {userProjectAccess['user_id'].id}")
        url = str(userProjectAccess['user_id'].id) + \
            '/' + str(userProjectAccess['project_id'].id)
        userProjectAccess['access_url'] = url
        userProjectAccess['otp'] = 0000

        if (userProjectAccess['user_id'] is None):
            raise serializers.ValidationError(
                {'error': 'User Project Access must have a user id', 'status': 400})
        if (userProjectAccess['project_id'] is None):
            raise serializers.ValidationError(
                {'error': 'User Project Access must have a project id', 'status': 400})
        # if (userProjectAccess['access_url'] is None):
        #     raise serializers.ValidationError(
        #         {'error': 'User Project Access must have a access url', 'status': 400})

        data = UserProjectAccess(**userProjectAccess)
        data.save()

        return data

    def update(self, instance, validated_data):
        instance.user_id = validated_data.get(
            'user_id', instance.user_id)
        instance.project_id = validated_data.get(
            'project_id', instance.project_id)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)
        instance.save()
        return instance
