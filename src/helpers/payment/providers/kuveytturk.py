"""Payment Provider APIs' Provider Classes"""

import base64
import hashlib
import urllib.parse
import uuid
import logging
import requests

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect
from apps.payment.models import DonationTransaction
from helpers.payment.providers.base import BasePaymentProvider

logger = logging.getLogger(__name__)

User = get_user_model()


class KuveytTurkPaymentProvider(BasePaymentProvider):
    RESPONSE_CODES = {
        "00": "Otorizasyon Verildi",
        "01": "Kartı Veren Bankayı Arayınız",
        "02": "Kartı Veren Bankayı Arayınız",
        "03": "Geçersiz Üye İşyeri",
        "04": "Karta el koyunuz",
        "05": "İşlem onaylanmadı",
        "09": "Tekrar Deneyiniz",
        "11": "VIP İşlem İçin Onay Verildi",
        "12": "Geçersiz İşlem",
        "13": "Geçersiz İşlem amountı",
        "14": "Geçersiz Kart Numarası",
        "15": "Kart Veren Banka Tanımsız",
        "33": "Vade Sonu Geçmiş Kart",
        "34": "Sahtekarlık",
        "36": "Kısıtlı Kart",
        "37": "Güvenliği Uyarınız, Karta El Konulmalı",
        "38": "Hatalı Şifre",
        "41": "Kayıp Kart - Karta El Konulmalı",
        "43": "Çalıntı Kart - Karta El Konulmalı",
        "51": "Bakiyesi - Kredisi Yetersiz",
        "53": "Döviz Hesabı Bulunamadı",
        "54": "Vade Sonu Geçmiş Kart",
        "55": "Hatalı Kart Şifresi",
        "56": "Kart Tanımlı Değil",
        "57": "İşlem Tipine İzin Yok",
        "58": "İşlem Tipi Terminale Kapalı",
        "59": "Sahtekarlık Şüphesi",
        "61": "Para Çekme - amount Limiti Aşıldı",
        "62": "Kısıtlanmış Kart",
        "63": "Güvenlik İhlali",
        "65": "Para Çekme Adet Limiti Aşıldı",
        "66": "İşlemi Reddediniz",
        "67": "Bu Hesapta Hiçbir İşlem Yapılamaz",
        "68": "Tanımsız Şube",
        "75": "Şifre Deneme Sayısı Aşıldı",
        "76": "Şifreler Uyuşmuyor",
        "77": "Şifre Script Talebi Reddedildi",
        "78": "Şifre Güvenilir Bulunmadı",
        "79": "ARQC Güvenlik Kontrolü Başarısız",
        "85": "Şifre Değişikliği / YÜkleme Onay",
        "88": "İşlem Şüpheli Tamamlandı",
        "89": "Ek Kart İle Bu İşlem Yapılamaz",
        "90": "Gün Sonu Devam Ediyor",
        "91": "Kartı Veren Banka Hizmet Dışı",
        "92": "Kart Veren Banka Tanımlı Değil",
        "93": "AYARLANACAK",
        "96": "SİSTEM ARIZASI",
    }
    CONF = settings.KUVEYTTURK_CONF

    def make_payment(self, request, request_data):
        payment_request_data = self.payment_request_parser(request, request_data)
        merchant_order_id = str(
            uuid.uuid4()
        )  # it can be anything, we use uuid for uniqueness

        # create new transaction
        self.create_transaction(request, payment_request_data, merchant_order_id)
        ########### HASH Process #############
        hashed_password = base64.b64encode(
            hashlib.sha1(
                settings.KUVEYTTURK_CONF["password"].encode("ISO-8859-9")
            ).digest()
        ).decode()
        hashed_data = base64.b64encode(
            hashlib.sha1(
                f'{settings.KUVEYTTURK_CONF["store_no"]}{merchant_order_id}{payment_request_data.amount_sent_to_bank}{settings.KUVEYTTURK_CONF["ok_url"]}{settings.KUVEYTTURK_CONF["fail_url"]}{settings.KUVEYTTURK_CONF["username"]}{hashed_password}'.encode(
                    "ISO-8859-9"
                )
            ).digest()
        ).decode()

        mobile_phone_cc, mobile_phone_subscriber = self.parse_phone_number(
            payment_request_data.phone
        )

        ########### Payment Request #############
        # TODO: Implement the payment request; BillAddrCity, BillAddrCountry, BillAddrLine1, BillAddrPostCode, BillAddrState
        data = f"""<KuveytTurkVPosMessage xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                                    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                    <APIVersion>1.0.0</APIVersion>
                    <OkUrl>{str(settings.KUVEYTTURK_CONF["ok_url"])}</OkUrl>
                    <FailUrl>{str(settings.KUVEYTTURK_CONF["fail_url"])}</FailUrl>
                    <HashData>{hashed_data}</HashData>
                    <MerchantId>{int(settings.KUVEYTTURK_CONF['store_no'])}</MerchantId>
                    <CustomerId>{int(settings.KUVEYTTURK_CONF['customer_no'])}</CustomerId>
                    <DeviceData>
                        <DeviceChannel>02</DeviceChannel>
                        <ClientIP>{str(payment_request_data.client_ip_address)}</ClientIP>
                    </DeviceData>
                    <CardHolderData>
                        <BillAddrCity>{str(payment_request_data.state_province)}</BillAddrCity>
                        <BillAddrCountry>{str(payment_request_data.country_code)}</BillAddrCountry>
                        <BillAddrLine1>{str(payment_request_data.add_line)}</BillAddrLine1>
                        <BillAddrPostCode>{str(payment_request_data.postal_code)}</BillAddrPostCode>
                        <BillAddrState>{str(payment_request_data.state_code)}</BillAddrState>
                        <Email>{str(payment_request_data.email)}</Email>
                        <MobilePhone>
                            <Cc>{str(mobile_phone_cc)}</Cc>
                            <Subscriber>{str(mobile_phone_subscriber)}</Subscriber>
                        </MobilePhone>
                    </CardHolderData>
                    <UserName>{str(settings.KUVEYTTURK_CONF['username'])}</UserName>
                    <CardNumber>{str(payment_request_data.card_number)}</CardNumber>
                    <CardExpireDateYear>{str(payment_request_data.card_year)}</CardExpireDateYear>
                    <CardExpireDateMonth>{str(payment_request_data.card_month)}</CardExpireDateMonth>
                    <CardCVV2>{str(payment_request_data.card_cvc)}</CardCVV2>
                    <CardHolderName>{str(payment_request_data.card_holder_name)}</CardHolderName>
                    <CardType>{str(payment_request_data.card_type)}</CardType>
                    <TransactionType>Sale</TransactionType>
                    <InstallmentCount>{int('0')}</InstallmentCount>
                    <Amount>{int(payment_request_data.amount_sent_to_bank)}</Amount>
                    <DisplayAmount>{int(payment_request_data.amount_sent_to_bank)}</DisplayAmount>
                    <CurrencyCode>{str('0949')}</CurrencyCode>
                    <MerchantOrderId>{str(merchant_order_id)}</MerchantOrderId>
                    <TransactionSecurity>{int('3')}</TransactionSecurity>
                </KuveytTurkVPosMessage>
                """
        headers = {"Content-Type": "application/xml", "Content-Length": str(len(data))}
        r = requests.post(
            settings.KUVEYTTURK_CONF["payment_request_url"],
            data=data.encode("ISO-8859-9"),
            headers=headers,
        )
        logger.info(
            "Payment requested. Transaction merchant order id: %s with amount %s (%s)",
            merchant_order_id,
            payment_request_data.amount,
            payment_request_data.amount_sent_to_bank,
        )

        bank_response = HttpResponse(r)
        logger.info("Bank response in make_payment: %s", bank_response)
        return bank_response

    def approve_payment(self, request):
        """
        Approves the payment request
        """
        approve_res = request.POST.get("AuthenticationResponse")
        approve_res = urllib.parse.unquote(approve_res)
        amount_start = approve_res.find("<Amount>")
        amount_end = approve_res.find("</Amount>")
        amount = approve_res[amount_start + 8 : amount_end]
        merchant_order_id_start = approve_res.find("<MerchantOrderId>")
        merchant_order_id_end = approve_res.find("</MerchantOrderId>")
        merchant_order_id = approve_res[
            merchant_order_id_start + 17 : merchant_order_id_end
        ]
        md_start = approve_res.find("<MD>")
        md_end = approve_res.find("</MD>")
        md = approve_res[md_start + 4 : md_end]
        hashed_password = base64.b64encode(
            hashlib.sha1(
                settings.KUVEYTTURK_CONF["password"].encode("ISO-8859-9")
            ).digest()
        ).decode()
        hashed_data = base64.b64encode(
            hashlib.sha1(
                f'{settings.KUVEYTTURK_CONF["store_no"]}{merchant_order_id}{amount}{settings.KUVEYTTURK_CONF["username"]}{hashed_password}'.encode(
                    "ISO-8859-9"
                )
            ).digest()
        ).decode()
        data = f"""
                <KuveytTurkVPosMessage xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:xsd="http://www.w3.org/2001/XMLSchema">
            <APIVersion>1.0.0</APIVersion>
            <HashData>{hashed_data}</HashData>
            <MerchantId>{int(settings.KUVEYTTURK_CONF['store_no'])}</MerchantId>
            <CustomerId>{int(settings.KUVEYTTURK_CONF['customer_no'])}</CustomerId>
            <UserName>{str(settings.KUVEYTTURK_CONF['username'])}</UserName>
            <TransactionType>Sale</TransactionType>
            <InstallmentCount>{int('0')}</InstallmentCount>
            <Amount>{int(amount)}</Amount>
            <MerchantOrderId>{str(merchant_order_id)}</MerchantOrderId>
            <TransactionSecurity>{int('3')}</TransactionSecurity>
            <KuveytTurkVPosAdditionalData>
            <AdditionalData>
            <Key>MD</Key>
            <Data>{str(md)}</Data>
            </AdditionalData>
             </KuveytTurkVPosAdditionalData>
            </KuveytTurkVPosMessage>
            """
        headers = {"Content-Type": "application/xml", "Content-Length": str(len(data))}
        r = requests.post(
            settings.KUVEYTTURK_CONF["payment_approve_url"],
            data=data.encode("ISO-8859-9"),
            headers=headers,
        )
        logger.info("Bank response in approve_payment: %s" % r)

        ##### Transaction Status Check #####
        response_code_start = r.text.find("<ResponseCode>")
        response_code_end = r.text.find("</ResponseCode>")
        response_code = str(r.text[response_code_start + 14 : response_code_end])

        ####### DonationTransaction get instance from payment ##############
        transaction = DonationTransaction.objects.filter(
            merchant_order_id=str(merchant_order_id)
        ).first()
        if transaction is None:
            logger.warning(
                "There is no transaction with merchant order id: %s", merchant_order_id
            )
        else:
            transaction.status_code = response_code
            transaction.status_code_description = (
                self.RESPONSE_CODES[response_code]
                if self.RESPONSE_CODES[response_code]
                else f"{str(response_code)}"
            )
            transaction.md_code = md

            if response_code == "00":
                transaction.is_complete = True

            transaction.save()

            if transaction.is_complete:
                query_string = urllib.parse.urlencode(
                    {
                        "details": "Bağışınız tamamlandı.",
                        "bank_status_code": transaction.status_code,
                        "bank_status_code_description": transaction.status_code_description,
                    }
                )
                redirect_url = f"{settings.APP_PAYMENT_RESPONSE_URL}?{query_string}"  # front end app will handle this response by using query string
                logger.info(
                    "Payment approved. Transaction merchant order id: %s with amount %s",
                    transaction.merchant_order_id,
                    transaction.amount,
                )
                return redirect(redirect_url)
        query_string = urllib.parse.urlencode(
            {
                "details": "Bağışınız tamamlanamadı.",
                "bank_status_code": transaction.status_code,
                "bank_status_code_description": transaction.status_code_description,
            }
        )
        redirect_url = f"{settings.APP_PAYMENT_RESPONSE_URL}?{query_string}"  # front end app will handle this response by using query string
        logger.warning(
            "Payment couldn't approved. Bank status code: %s - %s. Transaction merchant order id: %s with amount %s",
            transaction.status_code,
            transaction.status_code_description,
            transaction.merchant_order_id,
            transaction.amount,
        )
        return redirect(redirect_url)

    def payment_fail(self, request):
        """
        Payment fail view
        """
        approve_res = request.POST.get("AuthenticationResponse")
        approve_res = urllib.parse.unquote(approve_res)

        merchant_order_id_start = approve_res.find("<MerchantOrderId>")
        merchant_order_id_end = approve_res.find("</MerchantOrderId>")
        merchant_order_id = approve_res[
            merchant_order_id_start + 17 : merchant_order_id_end
        ]

        response_code_start = approve_res.find("<ResponseCode>")
        response_code_end = approve_res.find("</ResponseCode>")
        response_code = str(approve_res[response_code_start + 14 : response_code_end])

        response_message = approve_res.find("<ResponseMessage>")
        response_message_end = approve_res.find("</ResponseMessage>")
        response_message = str(
            approve_res[response_message + 17 : response_message_end]
        )

        # get the donation transaction instance
        transaction = DonationTransaction.objects.filter(
            merchant_order_id=str(merchant_order_id)
        ).first()
        if transaction is None:
            logger.warning(
                "There is no transaction with merchant order id: %s", merchant_order_id
            )
        else:
            # update the transaction status and save
            transaction.status_code = response_code
            transaction.status_code_description = response_message
            transaction.save()

        query_string = urllib.parse.urlencode(
            {
                "details": "Bağışınız tamamlanamadı.",
                "bank_status_code": transaction.status_code,
                "bank_status_code_description": transaction.status_code_description,
            }
        )
        redirect_url = f"{settings.APP_PAYMENT_RESPONSE_URL}?{query_string}"  # front end app will handle this response by using query string
        logger.warning(
            "Payment failed. Bank status code: %s - %s. Transaction merchant order id: %s with amount %s",
            transaction.status_code,
            transaction.status_code_description,
            transaction.merchant_order_id,
            transaction.amount,
        )
        return redirect(redirect_url)
