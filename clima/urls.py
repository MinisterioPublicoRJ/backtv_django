
from django.urls import path

from clima.views import ClimaView


app_name = 'clima'
urlpatterns = [
    path('clima/', ClimaView.as_view(), name='api-clima')
]
