import base64
import hashlib
import urllib.parse

import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from apps.donor.models import DonationTransaction


class KuveytTurkPaymentProvider(object):
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

    def payment_request_parser(self, request_data):
        """
            request_data (OrderedDict): Serialized data
        """
        ####### Bagisci Bilgileri #######
        name = request_data.get("name")
        email = request_data.get("email")
        phone = request_data.get("phone")
        amount = float(request_data.get("amount"))
        amount_sent_to_bank = amount * 100
        amount_sent_to_bank = str(amount_sent_to_bank)
        amount_sent_to_bank = int(amount_sent_to_bank.split(".")[0])

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
            raise ValueError('Please enter a valid card.')

        ####### Mesaj #######
        message = request_data.get("message")

        return {'name': name, 'email': email, 'phone': phone, 'amount': amount,
                'amount_sent_to_bank': amount_sent_to_bank, 'card_number': card_number,
                'card_holder_name': card_holder_name, 'card_expiry': card_expiry, 'card_date': card_date,
                'card_month': card_month,
                'card_year': card_year,
                'card_cvc': card_cvc,
                'card_type': card_type,
                'message': message
                }

    def make_payment(self, request, request_data):
        payment_request_data = self.payment_request_parser(request_data)
        merchant_order_id = f"web-bagis/STATIC-DEGISECEK/{str(timezone.now().time())}"  # istediğimiz değer yazılabilir bizim tuttuğumuz değer olacak (sabit veya değişken)
        ############## Bağış İşlem model instance create ##############
        new_transaction = DonationTransaction(
            name=payment_request_data['name'],
            email=payment_request_data['email'],
            phone=payment_request_data['phone'],
            amount=payment_request_data['amount'],
            amount_sent_to_bank=payment_request_data['amount_sent_to_bank'],
            merchant_order_id=merchant_order_id,
            message=payment_request_data['message'],
        )
        if request.user.is_authenticated:
            new_transaction.user = request.user
        new_transaction.save()
        ########### HASH Işlemleri #############
        hashed_password = base64.b64encode(
            hashlib.sha1(settings.KUVEYTTURK_CONF["password"].encode("ISO-8859-9")).digest()
        ).decode()
        hashed_data = base64.b64encode(
            hashlib.sha1(
                f'{settings.KUVEYTTURK_CONF["magaza_no"]}{merchant_order_id}{payment_request_data["amount"]}{settings.KUVEYTTURK_CONF["ok_url"]}{settings.KUVEYTTURK_CONF["fail_url"]}{settings.KUVEYTTURK_CONF["username"]}{hashed_password}'.encode(
                    "ISO-8859-9"
                )
            ).digest()
        ).decode()
        data = f"""
           <KuveytTurkVPosMessage xmlns:xsi="http://www.w3.org/2001/XMLSchemainstance"
           xmlns:xsd="http://www.w3.org/2001/XMLSchema">
           <APIVersion>1.0.0</APIVersion>
           <OkUrl>{str(settings.KUVEYTTURK_CONF["ok_url"])}</OkUrl>
           <FailUrl>{str(settings.KUVEYTTURK_CONF["fail_url"])}</FailUrl>
           <HashData>{hashed_data}</HashData>
           <MerchantId>{int(settings.KUVEYTTURK_CONF['magaza_no'])}</MerchantId>
           <CustomerId>{int(settings.KUVEYTTURK_CONF['musteri_no'])}</CustomerId>
           <UserName>{str(settings.KUVEYTTURK_CONF['username'])}</UserName>
           <CardNumber>{str(payment_request_data['card_number'])}</CardNumber>
           <CardExpireDateYear>{str(payment_request_data['card_year'])}</CardExpireDateYear>
           <CardExpireDateMonth>{str(payment_request_data['card_month'])}</CardExpireDateMonth>
           <CardCVV2>{str(payment_request_data['card_cvc'])}</CardCVV2>
           <CardHolderName>{str(payment_request_data['card_holder_name'])}</CardHolderName>
           <CardType>{str(payment_request_data['card_type'])}</CardType>
           <TransactionType>Sale</TransactionType>
           <InstallmentCount>{int('0')}</InstallmentCount>
           <Amount>{int(payment_request_data['amount_sent_to_bank'])}</Amount>
           <DisplayAmount>{int(payment_request_data['amount_sent_to_bank'])}</DisplayAmount>
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
        return HttpResponse(r)

    def approve_payment(self, request):
        approve_res = request.POST.get("AuthenticationResponse")
        approve_res = urllib.parse.unquote(approve_res)
        amount_start = approve_res.find("<Amount>")
        amount_end = approve_res.find("</Amount>")
        amount = approve_res[amount_start + 8: amount_end]
        merchant_order_id_start = approve_res.find("<MerchantOrderId>")
        merchant_order_id_end = approve_res.find("</MerchantOrderId>")
        merchant_order_id = approve_res[merchant_order_id_start + 17: merchant_order_id_end]
        md_start = approve_res.find("<MD>")
        md_end = approve_res.find("</MD>")
        md = approve_res[md_start + 4: md_end]
        hashed_password = base64.b64encode(
            hashlib.sha1(settings.KUVEYTTURK_CONF["password"].encode("ISO-8859-9")).digest()
        ).decode()
        hashed_data = base64.b64encode(
            hashlib.sha1(
                f'{settings.KUVEYTTURK_CONF["magaza_no"]}{merchant_order_id}{amount}{settings.KUVEYTTURK_CONF["username"]}{hashed_password}'.encode(
                    "ISO-8859-9"
                )
            ).digest()
        ).decode()
        data = f"""
                <KuveytTurkVPosMessage xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:xsd="http://www.w3.org/2001/XMLSchema">
            <APIVersion>1.0.0</APIVersion>
            <HashData>{hashed_data}</HashData>
            <MerchantId>{int(settings.KUVEYTTURK_CONF['magaza_no'])}</MerchantId>
            <CustomerId>{int(settings.KUVEYTTURK_CONF['musteri_no'])}</CustomerId>
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

        ##### transaction Durum Kontrol #####
        response_code_start = r.text.find("<ResponseCode>")
        response_code_end = r.text.find("</ResponseCode>")
        response_code = str(r.text[response_code_start + 14: response_code_end])

        ####### Bağış İşlem get instance ##############
        transaction = get_object_or_404(DonationTransaction, merchant_order_id=str(merchant_order_id))
        transaction.status_code = response_code
        transaction.status_code_description = self.RESPONSE_CODES[response_code] if self.RESPONSE_CODES[
            response_code] else f"{str(response_code)}"
        transaction.md_code = md

        if response_code == "00":
            transaction.is_complete = True

        transaction.save()

        return transaction.md_code
