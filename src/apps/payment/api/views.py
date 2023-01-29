from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.payment.api.serializers import CartSerializer
from apps.payment.models import Cart


class CartRetrieveAPIView(RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    lookup_field = 'pk'
