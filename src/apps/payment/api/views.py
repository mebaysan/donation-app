from rest_framework.generics import RetrieveAPIView

from apps.payment.api.serializers import CartSerializer
from apps.payment.models import Cart


class CartRetrieveAPIView(RetrieveAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    lookup_field = 'pk'
