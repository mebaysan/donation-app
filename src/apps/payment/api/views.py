from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import (
    RetrieveAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from apps.payment.api.serializers import (
    CartSerializer,
    CartItemSerializer,
    DonationSerializer,
    DonationTransactionSerializer,
    DonationTransactionDetailsSerializer,
)
from apps.payment.models import Cart, CartItem, Donation, DonationTransaction
from helpers.payment_provider.payment_provider_factory import PaymentProviderFactory


class DonationListAPIView(ListAPIView):
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # donations that are not in the cart
        return Donation.objects.filter(user=self.request.user).all()


class DonationTransactionListAPIView(ListAPIView):
    serializer_class = DonationTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            DonationTransaction.objects.filter(user=self.request.user)
            .all()
            .order_by("-date")
        )


class DonationTransactionRetrieveAPIView(RetrieveAPIView):
    serializer_class = DonationTransactionDetailsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        return DonationTransaction.objects.filter(user=self.request.user)


class CartRetrieveAPIView(RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.cart

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).first().cart_items.all()


class CartItemCreateAPIView(CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(cart=self.request.user.cart)


class CartItemRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Donation in the cart can be
     - added
     - retrieved (details)
     - removed
    """

    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user).all()


class CartClearAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = request.user.cart
        cart.cart_items.all().delete()
        return Response(
            status=status.HTTP_200_OK, data={"detail": "Sepet başarıyla temizlendi."}
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def payment(request):
    # Get payment provider payment request serializer class
    serializer_class = (
        PaymentProviderFactory.get_payment_provider_payment_request_serializer()
    )

    serializer = serializer_class(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    payment_data = serializer.validated_data
    provider = PaymentProviderFactory.get_payment_provider()
    return provider.make_payment(request, payment_data)


@api_view(["POST"])
@permission_classes([AllowAny])
def payment_success(request):
    provider = PaymentProviderFactory.get_payment_provider()
    return provider.approve_payment(request)


@api_view(["POST"])
@permission_classes([AllowAny])
def payment_fail(request):
    content = {"detail": "Payment failed!"}
    return Response(content, status.HTTP_400_BAD_REQUEST)
