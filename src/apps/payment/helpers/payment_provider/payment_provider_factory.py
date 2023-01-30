from apps.payment.helpers.payment_provider.providers.kuveytturk import KuveytTurkPaymentProvider
from apps.payment.models import PaymentProvider


class PaymentProviderFactory:
    @classmethod
    def get_published_payment_provider_instance(cls):
        return PaymentProvider.objects.filter(is_provider=True).first()

    @classmethod
    def get_payment_provider(cls):
        provider = cls.get_published_payment_provider_instance()
        if provider.name == 'KuveytTurk':
            return KuveytTurkPaymentProvider()
        else:
            return KuveytTurkPaymentProvider()
