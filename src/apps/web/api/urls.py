from django.urls import path, include

app_name = 'web_api'

urlpatterns = [
    path('donor/', include('apps.donor.api.urls')),
]
