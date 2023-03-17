from django.conf import settings


def get_app_name(request):
    return dict(get_app_name=str(settings.APP_NAME))
