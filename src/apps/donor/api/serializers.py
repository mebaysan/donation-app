from rest_framework import serializers

from apps.donor.models import DonationCategory, DonationItem, Donation, DonationTransaction


class DonationItemUnderCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationItem
        fields = ['name', 'description', 'image', 'is_published', 'category']


class DonationCategoryDetailsSerializer(serializers.ModelSerializer):
    items = DonationItemUnderCategorySerializer(many=True)

    class Meta:
        model = DonationCategory
        fields = ['name', 'description', 'image', 'is_published', 'items']


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
