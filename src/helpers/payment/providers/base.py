"""Payment Provider APIs' Base Provider Class"""

import uuid
import logging
from abc import ABC, abstractmethod
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response

from apps.management.models import BillAddress, Country
from apps.payment.models import DonationTransaction, Donation
from helpers.communication.email import send_password_reset_email
from helpers.payment.request import PaymentRequestData

logger = logging.getLogger(__name__)

User = get_user_model()


class BasePaymentProvider(ABC):
    """
    Base class for payment providers
    """

    def payment_request_parser(self, request, request_data) -> PaymentRequestData:
        """
        Parses the payment request data and returns a dictionary

        Args:
            request_data (OrderedDict): Serialized data

        Returns:
            PaymentRequestData: Parsed data
        """
        return PaymentRequestData.from_request_data(request, request_data)

    @abstractmethod
    def make_payment(self, request, request_data):
        """
        Makes the payment request to the payment provider

        This can be a different method for each payment provider
        """
        raise NotImplementedError

    def create_transaction(
        self, request, payment_request_data: PaymentRequestData, merchant_order_id
    ):
        """
        Creates a DonationTransaction instance

        Payment transaction will be connected to this instance

        Args:
            request (Request): Request object
            payment_request_data (PaymentRequestData): Parsed payment request data
            merchant_order_id (str): Merchant order id

        Returns:
            DonationTransaction: Created instance
        """

        new_transaction = DonationTransaction(
            first_name=payment_request_data.first_name,
            last_name=payment_request_data.last_name,
            email=payment_request_data.email,
            phone_number=payment_request_data.phone,
            amount=payment_request_data.amount,
            amount_sent_to_bank=payment_request_data.amount_sent_to_bank,
            merchant_order_id=merchant_order_id,
            message=payment_request_data.message,
            group_name=payment_request_data.group_name,
            organization_name=payment_request_data.organization_name,
            client_ip_address=payment_request_data.client_ip_address,
            country=payment_request_data.country,
            country_code=payment_request_data.country_code,
            state_province=payment_request_data.state_province,
            state_code=payment_request_data.state_code,
            add_line=payment_request_data.add_line,
            postal_code=payment_request_data.postal_code,
        )
        if request.user.is_authenticated:
            new_transaction.user = request.user

        else:  # payment request has no user (not logged-in)
            exists_user = User.objects.filter(
                email=payment_request_data.email,
                phone_number=payment_request_data.phone,
            ).first()
            if exists_user is not None:  # there is a User with credentials
                new_transaction.user = exists_user
            else:  # there is no User with the mail_templates or phone_number
                try:
                    new_user = User.objects.create(
                        first_name=payment_request_data.first_name,
                        last_name=payment_request_data.last_name,
                        email=payment_request_data.email,
                        username=payment_request_data.email,
                        phone_number=payment_request_data.phone,
                    )
                    new_user.set_password(str(uuid.uuid4()))
                    new_user.save()
                    new_transaction.user = new_user
                    send_password_reset_email(new_user)
                    new_billing_address = self.create_a_bill_address_for_new_user(
                        payment_request_data, new_user
                    )
                    logger.info(
                        "New user is created with a new billing address: %s - %s"
                        % (str(new_user), str(new_billing_address))
                    )
                except IntegrityError as e:
                    # mail_templates != phone_number for User
                    context = {
                        "details": "Lütfen geçerli email ve telefon numarası kullanın."
                    }
                    if "phone_number" in str(
                        e
                    ):  # email is different but phone_number is taken by a User
                        context["details"] = (
                            "Telefon farklı bir bağışçı profilinde kullanılıyor. Lütfen hesabınıza tanımlı email ve telefon numarasını kullanın."
                        )
                    if "username" in str(
                        e
                    ):  # phone_number is different but email (username) is taken by a User
                        context["details"] = (
                            "Email farklı bir bağışçı profilinde kullanılıyor. Lütfen hesabınıza tanımlı email ve telefon numarasını kullanın."
                        )
                    # TODO: this causes Server Error (500) because of the response type in Caprover setup...
                    return Response(context, status.HTTP_400_BAD_REQUEST)

        new_transaction.save()

        # create donations for the transaction
        self.create_donation(payment_request_data, new_transaction)

        return new_transaction

    def create_donation(
        self, payment_request_data: PaymentRequestData, new_transaction
    ):
        """
        Creates Donation instances for the transaction
        """
        for donation in payment_request_data.donations:
            new_donation = Donation.objects.create(
                donation_item=donation.get("donation_item"),
                amount=donation.get("amount"),
                donation_transaction=new_transaction,
                user=new_transaction.user,
            )
            new_donation.save()

    def parse_phone_number(self, phone_number):
        """
        Parses the phone number to split country code and phone number

        Args:
            phone_number (str): Phone number, +905555555555

        Returns:
            str, str: Country code excluded +, Phone number
        """
        country_code = phone_number[1:3]
        phone_number = phone_number[3:]
        return country_code, phone_number

    def create_a_bill_address_for_new_user(self, payment_request_data, new_user):
        country_obj = Country.objects.filter(
            country_code_alpha3=payment_request_data.country_code
        ).first()
        state_province_obj = country_obj.state_provinces.filter(
            state_code=payment_request_data.state_code
        ).first()
        bill_address = BillAddress(
            user=new_user,
            address_name="Ilk Adres",
            country=country_obj,
            state_province=state_province_obj,
            add_line=payment_request_data.add_line,
            postal_code=payment_request_data.postal_code,
        )
        bill_address.save()
        return bill_address
