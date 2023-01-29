from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.payment.api.serializers import CartSerializer
from apps.payment.models import Cart


class CartRetrieveAPIView(RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.cart

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).first().donations.all()
