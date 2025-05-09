from apps.payment.models import PaymentProvider
from apps.payment.api.serializers import KuveytTurkPaymentRequestSerializer
from helpers.payment.providers.kuveytturk import KuveytTurkPaymentProvider


class PaymentProviderFactory:
    @classmethod
    def get_published_payment_provider_instance(cls):
        """
        get published payment provider obj
        """
        return PaymentProvider.objects.filter(is_provider=True).first()

    @classmethod
    def get_payment_provider(cls):
        """
        Return Published Payment Provider Class
        """
        provider = cls.get_published_payment_provider_instance()

        if provider.code_name == "KT":
            return KuveytTurkPaymentProvider()
        return KuveytTurkPaymentProvider()  # for now we return KuveytTurk for default

    @classmethod
    def get_payment_provider_payment_request_serializer(cls):
        """
        Return Published Payment Provider's Serializer Class
        """
        provider = cls.get_published_payment_provider_instance()
        if provider and provider.code_name == "KT":
            return KuveytTurkPaymentRequestSerializer
        return KuveytTurkPaymentRequestSerializer  # for now we return KuveytTurk for default
