from django.urls import path

from orgaos.views import OrgaosView


app_name = 'orgaos'
urlpatterns = [
    path('orgaos/', OrgaosView.as_view(), name='api-list-orgaos'),
]
