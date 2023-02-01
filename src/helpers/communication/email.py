from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()


def send_email(subject, body, to_emails, ):
    email = EmailMessage(
        subject,
        body,
        settings.EMAIL_HOST_USER,
        to_emails
    )
    email.send()


def send_password_reset_email(user, request):
    current_site = get_current_site(request)
    subject = 'İhya Vakfı Bağışçı Hesabınız İçin Parola Sıfırlama Formu'
    message = render_to_string('mail_templates/password_reset.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    recipient_list = [user.email]
    send_email(subject, message, recipient_list)
