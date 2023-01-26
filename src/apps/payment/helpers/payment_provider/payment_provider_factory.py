from apps.payment.helpers.payment_provider.providers.kuveytturk import KuveytTurkPaymentProvider
from apps.payment.models import PaymentProvider


class PaymentProviderFactory:
    @classmethod
    def get_payment_provider(cls):
        provider = PaymentProvider.objects.filter(is_provider=True).first()
        if provider.name == 'KuveytTurk':
            return KuveytTurkPaymentProvider()
        else:
            return KuveytTurkPaymentProvider()
