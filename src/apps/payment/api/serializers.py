from rest_framework import serializers

from apps.payment.models import Cart, CartItem, Donation, DonationTransaction
from helpers.serializers.validators import email_regex, phone_regex, card_expiry_regex


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'


class DonationTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationTransaction
        fields = '__all__'


class DonationTransactionDetailsSerializer(serializers.ModelSerializer):
    donations = DonationSerializer(many=True)

    class Meta:
        model = DonationTransaction
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'donation_item', 'amount', 'added_date']


class CartItemPaymentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['donation_item', 'amount']


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['updated_date', 'amount', 'cart_items']


class PaymentRequestSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField(validators=[email_regex])
    phone = serializers.CharField(validators=[phone_regex])
    # amount = serializers.FloatField(min_value=0) # we sum manually in the provider method
    card_number = serializers.CharField(max_length=19)
    card_holder_name = serializers.CharField()
    card_expiry = serializers.CharField(max_length=5, validators=[card_expiry_regex])
    card_cvc = serializers.CharField(max_length=4)
    message = serializers.CharField(required=False)
    donations = CartItemPaymentRequestSerializer(many=True)

    def validate_card_number(self, value):
        """
            4      => Visa
            5 || 6 => MasterCard
            9      => Troy
        """
        if value[0] not in ["4", "5", "6", "9"]:
            raise serializers.ValidationError('Please enter a valid card.')
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Please enter a positive amount.')
        return value


class KuveytTurkPaymentRequestSerializer(PaymentRequestSerializer):
    pass
