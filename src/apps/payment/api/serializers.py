from rest_framework import serializers

from apps.donor.api.serializers import DonationSerializer
from apps.payment.models import Cart


class CartSerializer(serializers.ModelSerializer):
    donations = DonationSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['updated_date', 'amount', 'donations']
