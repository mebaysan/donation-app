from rest_framework import serializers

from apps.payment.models import Cart


# Serializers define the API representation.
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
