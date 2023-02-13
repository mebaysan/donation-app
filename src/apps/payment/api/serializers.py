from rest_framework import serializers

from apps.donor.models import DonationItem
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

    def validate_amount(self, value):
        donation_item_id = self.initial_data.get('donation_item')
        donation_item = DonationItem.objects.filter(id=donation_item_id).first()
        if donation_item.donation_type == 'Static':
            # donation item has rules
            if value < donation_item.quantity_price:
                raise serializers.ValidationError("Amount can't be less than the donation item's quantity price.")
            if value % donation_item.quantity_price != 0:
                raise serializers.ValidationError("Amount has to be multiple of donation item's quantity price.")
        return value


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
    phone_number = serializers.CharField(validators=[phone_regex])
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
            raise serializers.ValidationError('Lütfen geçerli bir kart girin.')
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("0'dan büyük bir sayı girin.")
        return value

    def validate_donations(self, value):
        for item in value:
            donation_item = DonationItem.objects.filter(id=item['donation_item'].id).first()
            if donation_item.donation_type == 'Static':
                if item['amount'] < donation_item.quantity_price:
                    raise serializers.ValidationError(
                        f"Amount can't be less than the donation item's quantity price. {item['amount']} is not acceptable for {item['donation_item'].name}.")
                if item['amount'] % donation_item.quantity_price != 0:
                    raise serializers.ValidationError(
                        f"Amount has to be multiple of donation item's quantity price. {item['amount']} is not acceptable for {item['donation_item'].name}.")
        return value


class KuveytTurkPaymentRequestSerializer(PaymentRequestSerializer):
    pass
