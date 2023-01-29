from rest_framework import serializers

from apps.donor.models import DonationCategory, DonationItem, Donation, DonationTransaction


class DonationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationCategory
        fields = '__all__'


class DonationItemSerializer(serializers.ModelSerializer):
    category = DonationCategorySerializer()

    class Meta:
        model = DonationItem
        fields = '__all__'


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        exclude = ['cart']


class DonationTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationTransaction
        fields = '__all__'
