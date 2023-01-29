from rest_framework.generics import (ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from apps.donor.api.serializers import (DonationCategorySerializer, DonationItemSerializer, DonationSerializer,
                                        DonationTransactionSerializer, DonationTransactionDetailsSerializer)
from apps.donor.models import DonationCategory, DonationItem, Donation, DonationTransaction


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
        # donations that are not in the cart
        return Donation.objects.exclude(cart=self.request.user.cart).all()

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


class DonationTransactionListAPIView(ListAPIView):
    serializer_class = DonationTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DonationTransaction.objects.filter(user=self.request.user).all()


class DonationTransactionRetrieveAPIView(RetrieveAPIView):
    serializer_class = DonationTransactionDetailsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return DonationTransaction.objects.filter(user=self.request.user)
