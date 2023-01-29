from rest_framework import serializers

from apps.donor.models import DonationCategory, DonationItem


class DonationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationCategory
        fields = '__all__'


class DonationItemSerializer(serializers.ModelSerializer):
    category = DonationCategorySerializer()

    class Meta:
        model = DonationItem
        fields = '__all__'
