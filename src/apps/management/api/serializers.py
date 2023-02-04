from django.contrib.auth import get_user_model
from rest_framework import serializers

from helpers.serializers.validators import email_regex, phone_regex, username_regex

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(validators=[phone_regex], max_length=17)

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions', 'is_superuser', 'is_staff', 'is_active', 'password']


class UserRegisterSerializer(serializers.ModelSerializer):
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
            raise serializers.ValidationError("Parolalar eşleşmiyor.")
        if data['username'] != data['email']:
            raise serializers.ValidationError("Kullanıcı adı ve email eşleşmiyor.")
        return data


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("Parolalar eşleşmiyor.")
        return data


class ObtainTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
