from rest_framework import serializers
from .models import Company


class CompanyRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('name', 'email_address', 'mobile_num')

    def create(self, validated_data):

        company = {}
        company['name'] = validated_data.get('name')
        company['email_address'] = validated_data.get('email_address')
        company['mobile_num'] = validated_data.get('mobile_num')

        if (company['name'] is None):
            raise serializers.ValidationError(
                {'error': 'Company must have a name', 'status': 400})
        if (company['email_address'] is None):
            raise serializers.ValidationError(
                {'error': 'Company must have a valid email address', 'status': 400})
        if (company['mobile_num'] is None):
            company['mobile_num'] = 0

        data = Company(**company)
        data.save()

        return data

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email_address = validated_data.get(
            'email_address', instance.email_address)
        instance.mobile_num = validated_data.get(
            'mobile_num', instance.mobile_num)
        instance.save()
        return instance
