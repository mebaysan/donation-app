from django.conf import settings


def get_app_name(request):
    return dict(get_app_name=settings.APP_NAME)


def get_favicon(request):
    return dict(get_favicon=settings.APP_FAVICON_URL)
