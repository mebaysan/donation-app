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
        exclude = ["user"]

    def validate_country_code(self, value):
        if (
            not Country.objects.filter(country_code_alpha3=value).first()
            and not Country.objects.filter(country_code=value).first()
        ):
            raise serializers.ValidationError("Invalid country code.")
        return value

    def validate_state_province(self, value):
        state_province_obj = StateProvince.objects.filter(id=value.id).first()
        if not state_province_obj:
            raise serializers.ValidationError("Invalid state province.")
        if str(state_province_obj.country.id) != str(self.initial_data.get("country")):
            raise serializers.ValidationError("Invalid state province for the country.")
        return value

    def validate_state_code(self, value):
        state_province_obj = StateProvince.objects.filter(state_code=value).first()
        if not state_province_obj:
            raise serializers.ValidationError("Invalid state code.")
        if (
            StateProvince.objects.filter(id=self.initial_data.get("state_province"))
            .first()
            .state_code
            != value
        ):
            raise serializers.ValidationError("State code and state province mismatch.")
        return value


class BillAddressListSerializer(BillAddressDetailsSerializer):
    country = CountrySerializer()
    state_province = StateProvinceSerializer()
