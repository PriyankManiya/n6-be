from rest_framework import serializers
from .models import  Credential, User

from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# example
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('email_address', 'password', 'password2', 'name', 'tc')

        extra_kwargs = {
            'password': {'write_only': True},
        }

    # Validating Password and Password2
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError(
                'Passwords and Confirm Password must match.')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



# class UserLoginSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(max_length=255, min_length=3)
#
#     class Meta:
#         model = User
#         fields = ('email', 'password')
#
#
# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'email', 'name', 'tc', 'created_at', 'updated_at', 'is_admin', 'is_active')
#         extra_kwargs = {
#             'id': {'read_only': True},
#             'email': {'read_only': True},
#             'created_at': {'read_only': True},
#             'updated_at': {'read_only': True},
#         }
#
#
# class UserChangePasswordSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
#     password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
#     old_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
#
#     class Meta:
#         model = User
#         fields = ('password', 'password2', 'old_password')
#         extra_kwargs = {
#             'password': {'write_only': True},
#         }
#
#     # Validating Password and Password2
#     def validate(self, attrs):
#         password = attrs.get('password')
#         password2 = attrs.get('password2')
#         user = self.context.get('user')
#
#         if password != password2:
#             raise serializers.ValidationError('Passwords and Confirm Password must match.')
#         user.set_password(password)
#         user.save()
#         return attrs
#
#
# class SendEmailSerializer(serializers.Serializer):
#     email = serializers.EmailField(max_length=255, min_length=3)
#     url = serializers.CharField(max_length=255, min_length=3, read_only=True)
#
#     class Meta:
#         model = User
#         fields = ('email', 'url')
#         extra_kwargs = {
#             'url': {'read_only': True},
#         }
#
#     def validate(self, attrs):
#         email = attrs.get('email')
#         if User.objects.filter(email=email).exists():
#             user = User.objects.get(email=email)
#             uid = urlsafe_base64_encode(force_bytes(user.id))
#             token = PasswordResetTokenGenerator().make_token(user)
#             url = 'http://127.0.0.1:8000/api/user/reset-password/' + uid + '/' + token + '/'
#             attrs['url'] = url
#
#             # Send Email
#             data = {
#                 'email_subject': 'Password Reset',
#                 'email_body': 'Hi ' + user.name + ', Please click on the link below to reset your password. ' + url,
#                 'email_to': email,
#             }
#
#             utils.Util.send_email(data=data)
#
#             return attrs
#
#         else:
#             raise serializers.ValidationError('Email does not exist.')
#
#     def create(self, validated_data):
#         return validated_data
#
#
# class ResetPasswordSerializer(serializers.Serializer):
#     password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
#     password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
#
#     class Meta:
#         model = User
#         fields = ('password', 'password2')
#
#     def validate(self, attrs):
#         try:
#             password = attrs.get('password')
#             password2 = attrs.get('password2')
#             token = self.context.get('token')
#             uid = smart_str(urlsafe_base64_decode(self.context.get('uid')))
#             user = User.objects.get(id=uid)
#
#             if password != password2:
#                 raise serializers.ValidationError('Password and Confirm Password must match.')
#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 raise serializers.ValidationError('Token is not valid or Expired. <<')
#             user.set_password(password)
#             user.save()
#             return attrs
#
#         except DjangoUnicodeDecodeError as identifier:
#             PasswordResetTokenGenerator().check_token(user, token)
#             raise serializers.ValidationError('Token is not valid or Expired. --', code='authorization')
#
#     def create(self, validated_data):
#         return validated_data
