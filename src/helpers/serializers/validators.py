from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r'^\+\d{1,3}\d{1,15}$',
    message="Phone number must be in the format: '+[country code][phone number]'"
)
email_regex = RegexValidator(
    regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$',
    message="Email must be in the format: 'example@domain.com'"
)

card_expiry_regex = RegexValidator(
    regex=r'^(0[1-9]|1[0-2])\/(\d{2})$',
    message="Card expiry must be in the format: 'MM/YY'"
)

username_regex = RegexValidator(
    regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$',
    message="Username must be in the format: 'example@domain.com'"
)
