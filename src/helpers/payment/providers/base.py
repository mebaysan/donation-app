"""Payment Provider APIs' Base Provider Class"""
import uuid
import logging
from abc import ABC, abstractmethod
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response

from apps.payment.models import DonationTransaction, Donation
from helpers.communication.email import send_password_reset_email

logger = logging.getLogger(__name__)

User = get_user_model()


class BasePaymentProvider(ABC):
    """
    Base class for payment providers
    """

    def payment_request_parser(self, request_data):
        """
        Parses the payment request data and returns a dictionary

        Args:
            request_data (OrderedDict): Serialized data

        Returns:
            dict: Parsed data
        """
        ####### Bagisci Bilgileri #######
        first_name = request_data.get("first_name")
        last_name = request_data.get("last_name")
        email = request_data.get("email")
        phone = request_data.get("phone_number")

        # ####### Kart Bilgileri #######
        card_number = request_data.get("card_number").replace(" ", "")
        card_holder_name = request_data.get("card_holder_name").upper()
        card_expiry = request_data.get("card_expiry")
        card_date = card_expiry.split("/")
        card_month = card_date[0].strip()
        card_year = card_date[1].strip()
        card_cvc = request_data.get("card_cvc")

        if card_number[0] == "4":
            card_type = "Visa"
        elif card_number[0] == "5" or card_number[0] == "6":
            card_type = "MasterCard"
        elif card_number[0] == "9":
            card_type = "Troy"
        else:
            raise ValueError("Lütfen geçerli bir kart girin.")

        ####### Mesaj #######
        message = request_data.get("message")

        ####### Donation Items #######
        donations = request_data.get("donations")

        ####### Amount #######
        amount = 0
        for donation in donations:
            amount += donation.get("amount")
        amount = float(amount)
        amount_sent_to_bank = amount * 100
        amount_sent_to_bank = str(amount_sent_to_bank)
        amount_sent_to_bank = int(amount_sent_to_bank.split(".")[0])

        ####### Donation Items #######
        group_name = request_data.get("group_name", None)
        organization_name = request_data.get("organization_name", None)

        return {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "amount": amount,
            "amount_sent_to_bank": amount_sent_to_bank,
            "card_number": card_number,
            "card_holder_name": card_holder_name,
            "card_expiry": card_expiry,
            "card_date": card_date,
            "card_month": card_month,
            "card_year": card_year,
            "card_cvc": card_cvc,
            "card_type": card_type,
            "message": message,
            "donations": donations,
            "group_name": group_name,
            "organization_name": organization_name,
        }

    @abstractmethod
    def make_payment(self, request, request_data):
        """
        Makes the payment request to the payment provider

        This can be a different method for each payment provider
        """
        raise NotImplementedError

    def create_transaction(self, request, payment_request_data, merchant_order_id):
        """
        Creates a DonationTransaction instance

        Payment transaction will be connected to this instance

        Args:
            request (Request): Request object
            payment_request_data (dict): Parsed payment request data
            merchant_order_id (str): Merchant order id

        Returns:
            DonationTransaction: Created instance
        """

        new_transaction = DonationTransaction(
            first_name=payment_request_data["first_name"],
            last_name=payment_request_data["last_name"],
            email=payment_request_data["email"],
            phone_number=payment_request_data["phone"],
            amount=payment_request_data["amount"],
            amount_sent_to_bank=payment_request_data["amount_sent_to_bank"],
            merchant_order_id=merchant_order_id,
            message=payment_request_data["message"],
            group_name=payment_request_data["group_name"],
            organization_name=payment_request_data["organization_name"],
        )
        if request.user.is_authenticated:
            new_transaction.user = request.user

        else:  # payment request has no user (not logged-in)
            exists_user = User.objects.filter(
                email=payment_request_data["email"],
                phone_number=payment_request_data["phone"],
            ).first()
            if exists_user is not None:  # there is a User with credentials
                new_transaction.user = exists_user
            else:  # there is no User with the mail_templates or phone_number
                try:
                    new_user = User.objects.create(
                        first_name=payment_request_data["first_name"],
                        last_name=payment_request_data["first_name"],
                        email=payment_request_data["email"],
                        username=payment_request_data["email"],
                        phone_number=payment_request_data["phone"],
                    )
                    new_user.set_password(str(uuid.uuid4()))
                    new_user.save()
                    new_transaction.user = new_user
                    send_password_reset_email(new_user)
                except IntegrityError as e:
                    # mail_templates != phone_number for User
                    context = {
                        "details": "Lütfen geçerli email ve telefon numarası kullanın."
                    }
                    if "phone_number" in str(
                        e
                    ):  # email is different but phone_number is taken by a User
                        context[
                            "details"
                        ] = "Telefon farklı bir bağışçı profilinde kullanılıyor. Lütfen hesabınıza tanımlı email ve telefon numarasını kullanın."
                    if "username" in str(
                        e
                    ):  # phone_number is different but email (username) is taken by a User
                        context[
                            "details"
                        ] = "Email farklı bir bağışçı profilinde kullanılıyor. Lütfen hesabınıza tanımlı email ve telefon numarasını kullanın."
                    # TODO: this causes Server Error (500) because of the response type in Caprover setup...
                    return Response(context, status.HTTP_400_BAD_REQUEST)

        new_transaction.save()

        # create donations for the transaction
        self.create_donation(payment_request_data, new_transaction)

        return new_transaction

    def create_donation(self, payment_request_data, new_transaction):
        """
        Creates Donation instances for the transaction
        """
        for donation in payment_request_data["donations"]:
            new_donation = Donation.objects.create(
                donation_item=donation.get("donation_item"),
                amount=donation.get("amount"),
                donation_transaction=new_transaction,
                user=new_transaction.user,
            )
            new_donation.save()

