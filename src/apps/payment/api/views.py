from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.payment.api.serializers import CartSerializer, CartItemSerializer
from apps.payment.helpers.payment_provider.payment_provider_factory import PaymentProviderFactory
from apps.payment.models import Cart, CartItem


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
    lookup_field = 'pk'

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user).all()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payment(request):
    provider = PaymentProviderFactory.get_payment_provider()
    return provider.make_payment(request)
    # return Response({"message": "Hello, world!"})
