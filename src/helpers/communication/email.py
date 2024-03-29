"""Email helper functions."""
import uuid
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

logger = logging.getLogger(__name__)

User = get_user_model()


def send_email(subject, body, to_emails, html_message=None):
    email = EmailMessage(
        subject,
        body,
        settings.EMAIL_HOST_USER,
        to_emails,
        reply_to=[settings.EMAIL_HOST_USER],
    )
    if html_message:
        email.content_subtype = "html"
        email.body = html_message
    email.send()


def send_password_reset_email(user):
    try:
        # change user's password randomly
        user.set_password(str(uuid.uuid4()))
        user.save()

        # send email
        subject = f"{settings.APP_NAME} Bağışçı Hesabınız İçin Parola Sıfırlama Formu"

        # generate url
        protocol = "https" if settings.DEBUG == False else "http"
        domain = settings.ALLOWED_HOSTS[0]
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        password_reset_url = (
            f"{ protocol }://{ domain }/api/password-reset/{ uid }/{ token }/"
        )
        message = render_to_string(
            "mail_templates/password_reset.html",
            {
                "user": user,
                "password_reset_url": password_reset_url,
                "app_name": settings.APP_NAME,
            },
        )
        recipient_list = [user.email]
        send_email(subject, message, recipient_list, html_message=message)
    except Exception as e:
        logger.error("Error while sending password reset email: %s", str(e))


def send_password_reset_success_email(user):
    # send email
    try:
        subject = f"{settings.APP_NAME} Bağışçı Hesabınız Hakkında Bilgilendirme"
        message = render_to_string(
            "mail_templates/message.html",
            {
                "user": user,
                "message": f"Bağışçı hesabınızın parolası güncellendi. Eğer işlem size ait değilse lütfen {settings.APP_NAME} ile iletişime geçin.",
                "app_name": settings.APP_NAME,
            },
        )
        recipient_list = [user.email]
        send_email(subject, message, recipient_list, html_message=message)
    except Exception as e:
        logger.error("Error while sending password reset success email: %s", str(e))
