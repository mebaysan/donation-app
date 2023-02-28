from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r"^\+\d{1,3}\d{1,15}$",
    message="Telefon numarası şu formatta olmalı: '+[ülke kodu][telefon numarası]'",
)
email_regex = RegexValidator(
    regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$",
    message="Email şu formatta olmalı: 'example@domain.com'",
)

card_expiry_regex = RegexValidator(
    regex=r"^(0[1-9]|1[0-2])\/(\d{2})$",
    message="Kart son kullanım tarihi şu formatta olmalı: 'MM/YY'",
)

username_regex = RegexValidator(
    regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$",
    message="Kullanıcı adı şu formatta olmalı: 'example@domain.com'",
)

MIN_PASSWORD_LENGTH = 12
