from django.urls import path

from orgaos.views import OrgaosListView


app_name = 'orgaos'
urlpatterns = [
    path('orgaos/', OrgaosListView.as_view(), name='api-list-orgaos'),
]
