from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.donor.api.serializers import DonationCategorySerializer, DonationItemSerializer
from apps.donor.models import DonationCategory, DonationItem


class DonationCategoryListAPIView(ListAPIView):
    serializer_class = DonationCategorySerializer
    queryset = DonationCategory.objects.filter(is_published=True).all()


class DonationCategoryRetrieveAPIView(RetrieveAPIView):
    serializer_class = DonationCategorySerializer
    queryset = DonationCategory.objects.filter(is_published=True).all()
    lookup_field = 'pk'


class DonationItemListAPIView(ListAPIView):
    serializer_class = DonationItemSerializer
    queryset = DonationItem.objects.filter(is_published=True).all()


class DonationItemRetrieveAPIView(RetrieveAPIView):
    serializer_class = DonationItemSerializer
    queryset = DonationItem.objects.filter(is_published=True).all()
    lookup_field = 'pk'
