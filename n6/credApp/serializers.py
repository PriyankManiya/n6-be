from rest_framework import serializers
from credApp.models import Credential
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.encoding import force_bytes
from django.contrib.auth.hashers import make_password
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from . import utils


class CredentialAppSerializer(serializers.ModelSerializer):

    class Meta:
        model = Credential
        fields = ('user_name', 'password',
                  'user', 'user_level', 'is_active')

    def create(self, validated_data):
        """
        It creates a new credential object and saves it to the database
        
        :param validated_data: The validated data from the serializer
        :return: The data is being returned.
        """

        cred = {}
        cred['user_name'] = validated_data.get('user_name')
        cred['password'] = validated_data.get('password')
        cred['user'] = validated_data.get('user')
        cred['user_level'] = validated_data.get('user_level')
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

        data = Credential(**cred)
        data.save()

        return data


class CredentialAppUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Credential
        fields = ('user_level', 'is_active')

    def update(self, instance, validated_data):
        """
        The update function is used to update an existing instance of the model.
        
        :param instance: The current instance of the object being updated
        :param validated_data: The data that was validated by the serializer
        :return: The instance is being returned.
        """
        instance.user_level = validated_data.get(
            'user_level', instance.user_level)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)
        instance.save()
        return instance


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Credential
        fields = ('user_name', 'password', 'password2',
                  'user', 'user_level')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        """
        If the password and confirm password don't match, raise a validation error
        
        :param attrs: The validated data from the serializer
        :return: The validated data.
        """
        password = attrs.get('password')
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError(
                'Passwords and Confirm Password must match.')
        return attrs

    def create(self, validated_data):
        """
        The function takes in a validated_data dictionary, and returns a new Credential object
        
        :param validated_data: The data that has been validated by the serializer
        :return: The user object is being returned.
        """
        user_name = validated_data['user_name']
        user = validated_data['user']
        user_level = validated_data['user_level']
        password = validated_data['password']

        if not user_name:
            raise ValueError('Users must have an user name')
        if not user:
            raise ValueError('Users must have an user id')
        if not user_level:
            raise ValueError('Users must have an user level id')

        user = Credential(
            user_name=user_name,
            user=user,
            user_level=user_level,
            password=make_password(password)
        )

        user.save()
        return user


class CredProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = ('id', 'user_name', 'user', 'user_level',
                  'updated_at', 'created_at', 'is_admin', 'is_active')
        extra_kwargs = {
            'password': {'write_only': True},
        }
        extra_kwargs = {
            'id': {'read_only': True},
            'user_name': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }


class CredLoginSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(max_length=255, min_length=3)

    class Meta:
        model = Credential
        fields = ('user_name', 'password')


class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    old_password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Credential
        fields = ('password', 'password2', 'old_password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        """
        If the password and confirm password don't match, raise a validation error. 
        
        If they do match, set the password and save the user. 
        
        The validation error is a built-in error that Django REST Framework provides. 
        
        The set_password() function is a built-in Django function that hashes the password. 
        
        The save() function is a built-in Django function that saves the user. 
        
        The attrs variable is a dictionary that contains the validated data. 
        
        The context variable is a dictionary that contains the request. 
        
        The user variable is the user that is currently logged in. 
        
        The password variable is the password that the user entered. 
        
        The password2 variable is the confirm password that the user entered. 
        
        The get() function is a built-in Django REST Framework function that gets the validated data. 
        
        The get() function is a built-
        
        :param attrs: The validated data from the serializer
        :return: The validated data.
        """
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')

        if password != password2:
            raise serializers.ValidationError(
                'Passwords and Confirm Password must match.')
        user.set_password(password)
        user.save()
        return attrs


class SendEmailSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=255, min_length=3)
    url = serializers.CharField(max_length=255, min_length=3, read_only=True)

    class Meta:
        model = Credential
        fields = ('user_name', 'url')
        extra_kwargs = {
            'url': {'read_only': True},
        }

    def validate(self, attrs):
        """
        If the user_name exists in the database, generate a token and send an email to the user
        
        :param attrs: The validated data from the serializer
        :return: The url is being returned.
        """
        user_name = attrs.get('user_name')
        if Credential.objects.filter(user_name=user_name).exists():
            cred = Credential.objects.get(user_name=user_name)
            cid = urlsafe_base64_encode(force_bytes(cred.id))
            token = PasswordResetTokenGenerator().make_token(cred)
            # url = 'http://127.0.0.1:8000/api/cred/reset-password/' + cid + '/' + token + '/'
            url = 'http://172.22.2.99:3000/reset-password-link/' + cid + '/' + token + '/'
            attrs['url'] = url

            # Send Email
            data = {
                'email_subject': 'Password Reset',
                'email_body': 'Hi ' + cred.user.first_name + ' ' + cred.user.last_name + ', Please click on the link below to reset your password. ' + url,
                'email_to': cred.user.email_address,
            }

            utils.Util.send_email(data=data)

            return attrs

        else:
            raise serializers.ValidationError('User Name does not exist.')

    """
    > The `create` function is called when a new instance of the model is created
    
    :param validated_data: The data that has been validated by the serializer
    :return: The validated data.
    """
    def create(self, validated_data):
        return validated_data


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Credential
        fields = ('password', 'password2')

    def validate(self, attrs):
        """
        It takes the token and the user id from the url, checks if the token is valid, and if it is, it
        sets the password to the new password
        
        :param attrs: The validated data from the serializer
        :return: The serializer is returning the validated data.
        """
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            token = self.context.get('token')
            cid = smart_str(urlsafe_base64_decode(self.context.get('cid')))
            cred = Credential.objects.get(id=cid)

            if password != password2:
                raise serializers.ValidationError(
                    'Password and Confirm Password must match.')
            if not PasswordResetTokenGenerator().check_token(cred, token):
                raise serializers.ValidationError(
                    'Token is not valid or Expired')
            cred.set_password(password)
            cred.save()
            return attrs

        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(cred, token)
            raise serializers.ValidationError(
                'Token is not valid or Expired', code='authorization')

    def create(self, validated_data):
        """
        It takes the validated data and returns it
        
        :param validated_data: The data that has been validated by the serializer
        :return: The validated data.
        """
        return validated_data
