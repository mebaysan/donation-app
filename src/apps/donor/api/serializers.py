from rest_framework import serializers

from apps.donor.models import DonationCategory, DonationItem, Bank, BankAccount


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


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'


class BankSerializer(serializers.ModelSerializer):
    bank_accounts = BankAccountSerializer(many=True)

    class Meta:
        model = Bank
        fields = '__all__'
