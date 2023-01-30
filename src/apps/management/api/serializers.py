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
    username = serializers.CharField(validators=[phone_regex], max_length=17)  # login should be only with phone number

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions', 'is_superuser', 'is_staff', 'is_active', 'password']


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
