from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    phone_regex = RegexValidator(
        regex=r'^\+\d{1,3}\d{1,15}$',
        message="Phone number must be in the format: '+[country code][phone number]'"
    )
    phone_number = serializers.CharField(validators=[phone_regex], max_length=17)

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions', 'is_superuser', 'is_staff', 'is_active', 'password']


class UserRegisterSerializer(serializers.ModelSerializer):
    phone_regex = RegexValidator(
        regex=r'^\+\d{1,3}\d{1,15}$',
        message="Phone number must be in the format: '+[country code][phone number]'"
    )
    email_regex = RegexValidator(
        regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$',
        message="Email must be in the format: 'example@domain.com'"
    )
    username_regex = RegexValidator(
        regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$',
        message="Username must be in the format: 'example@domain.com'"
    )
    phone_number = serializers.CharField(validators=[phone_regex], max_length=17, required=True)
    email = serializers.CharField(validators=[email_regex], required=True)
    username = serializers.CharField(validators=[username_regex], required=True)
    password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions', 'is_superuser', 'is_staff', 'is_active']

    def validate(self, data):
        if data['password'] != data['confirm_new_password']:
            raise serializers.ValidationError("New passwords do not match.")
        if data['username'] != data['email']:
            raise serializers.ValidationError("Username and email do not match.")
        return data


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("New passwords do not match.")
        return data


class ObtainTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
