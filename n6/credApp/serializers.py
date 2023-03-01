from rest_framework import serializers
from credApp.models import Credential


class CredentialAppSerializer(serializers.ModelSerializer):

    class Meta:
        model = Credential
        fields = ('user_name', 'password', 'active_tf',
                  'user', 'user_level')

    def create(self, validated_data):

        cred = {}
        cred['user_name'] = validated_data.get('user_name')
        cred['password'] = validated_data.get('password')
        cred['user'] = validated_data.get('user')
        cred['user_level'] = validated_data.get('user_level')
        cred['active_tf'] = validated_data.get('active_tf')
        print(f"cred['active_tf'] :: {cred['active_tf']}")
        if (cred['user_name'] is None):
            raise serializers.ValidationError(
                {'error': 'User must have User Name', 'status': 400})
        if (cred['password'] is None):
            raise serializers.ValidationError(
                {'error': 'User must have a valid password', 'status': 400})
        if (cred['user'] is None):
            raise serializers.ValidationError(
                {'error': 'User must have a valid user id', 'status': 400})
        if (cred['user_level'] is None):
            raise serializers.ValidationError(
                {'error': 'User must have a valid user level id', 'status': 400})
        if (cred['active_tf'] is None):
            {'error': 'User must have a valid Activation', 'status': 400}

        data = Credential(**cred)
        data.save()

        return data

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.email_address = validated_data.get(
    #         'email_address', instance.email_address)
    #     instance.mobile_num = validated_data.get(
    #         'mobile_num', instance.mobile_num)
    #     instance.save()
    #     return instance
