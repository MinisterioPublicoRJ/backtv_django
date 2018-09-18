from django.urls import path

from membro.views import MembroFotoView

app_name = 'membro'

urlpatterns = [
    path('membro/foto/', MembroFotoView.as_view(), name='api-foto'),
]
