from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.donor.api.serializers import DonationCategorySerializer, DonationItemSerializer, DonationSerializer
from apps.donor.models import DonationCategory, DonationItem, Donation


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


class DonationListCreateAPIView(ListCreateAPIView):
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Donation.objects.filter(cart=self.request.user.cart).all()

    def perform_create(self, serializer):
        serializer.save(cart=self.request.user.cart)


class DonationRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
        Donation in the cart can be
         - added
         - retrieved (details)
         - removed
    """
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return Donation.objects.filter(cart__user=self.request.user).all()
