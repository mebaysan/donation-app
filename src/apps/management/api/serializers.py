from django.contrib.auth import get_user_model
from rest_framework import serializers
from helpers.serializers.validators import (
    email_regex,
    phone_regex,
    username_regex,
    MIN_PASSWORD_LENGTH,
)
from apps.management.models import Country, StateProvince, BillAddress

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(validators=[phone_regex], max_length=17)
    get_total_amount_of_donations = serializers.DecimalField(
        max_digits=16, decimal_places=2
    )
    get_total_count_of_donations = serializers.IntegerField()

    class Meta:
        model = User
        exclude = [
            "groups",
            "user_permissions",
            "is_superuser",
            "is_staff",
            "is_active",
            "password",
        ]

    def validate(self, data):
        if data["username"] != data["email"]:
            raise serializers.ValidationError("Kullanıcı adı ve email eşleşmiyor.")
        return data


class UserRegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        validators=[phone_regex], max_length=17, required=True
    )
    email = serializers.CharField(validators=[email_regex], required=True)
    username = serializers.CharField(validators=[username_regex], required=True)
    password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        exclude = [
            "groups",
            "user_permissions",
            "is_superuser",
            "is_staff",
            "is_active",
        ]

    def validate(self, data):
        if data["password"] != data["confirm_new_password"]:
            raise serializers.ValidationError("Parolalar eşleşmiyor.")
        if data["username"] != data["email"]:
            raise serializers.ValidationError("Kullanıcı adı ve email eşleşmiyor.")

        # Password validation
        password = data.get("password")
        if password and len(password) < MIN_PASSWORD_LENGTH:
            raise serializers.ValidationError(
                f"Parola en az {MIN_PASSWORD_LENGTH} karakter uzunluğunda olmalıdır."
            )
        return data


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_new_password"]:
            raise serializers.ValidationError("Parolalar eşleşmiyor.")

        # Password validation
        password = data.get("password")
        if password and len(password) < MIN_PASSWORD_LENGTH:
            raise serializers.ValidationError(
                f"Parola en az {MIN_PASSWORD_LENGTH} karakter uzunluğunda olmalıdır."
            )
        return data


class ObtainTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class StateProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StateProvince
        fields = "__all__"


class CountryDetailSerializer(serializers.ModelSerializer):
    state_provinces = StateProvinceSerializer(many=True)

    class Meta:
        model = Country
        fields = [
            "id",
            "name",
            "country_code",
            "country_code_alpha3",
            "phone",
            "currency",
            "state_provinces",
        ]


class BillAddressDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillAddress
        fields = "__all__"


class BillAddressListSerializer(BillAddressDetailsSerializer):
    country = CountrySerializer()
    state_province = StateProvinceSerializer()

    class Meta:
        model = BillAddress
        fields = "__all__"
