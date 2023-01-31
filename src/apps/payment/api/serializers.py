from django.core.validators import RegexValidator
from rest_framework import serializers

from apps.payment.models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'donation_item', 'amount', 'added_date']


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['updated_date', 'amount', 'cart_items']


class PaymentRequestSerializer(serializers.Serializer):
    phone_regex = RegexValidator(
        regex=r'^\+\d{1,3}\d{1,15}$',
        message="Phone number must be in the format: '+[country code][phone number]'"
    )
    email_regex = RegexValidator(
        regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$',
        message="Email must be in the format: 'example@domain.com'"
    )

    name = serializers.CharField()
    email = serializers.EmailField(validators=[email_regex])
    phone = serializers.CharField(validators=[phone_regex])
    amount = serializers.FloatField(min_value=0)
    card_number = serializers.CharField(max_length=19)
    card_holder_name = serializers.CharField()
    card_expiry = serializers.CharField(max_length=7)
    card_cvc = serializers.CharField(max_length=4)
    message = serializers.CharField(required=False)

    def validate_card_number(self, value):
        if value[0] not in ["4", "5", "6", "9"]:
            raise serializers.ValidationError('Please enter a valid card.')
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Please enter a positive amount.')
        return value


class KuveytTurkPaymentRequestSerializer(PaymentRequestSerializer):
    pass
