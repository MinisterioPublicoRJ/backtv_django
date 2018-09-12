from django.urls import path

from orgaos.views import (
        OrgaosListView,
        VistasListView,
        AcervoView
        )


app_name = 'orgaos'
urlpatterns = [
    path('orgaos/', OrgaosListView.as_view(), name='api-list-orgaos'),
    path('orgaos/vistas/', VistasListView.as_view(), name='api-list-vistas'),
    path('orgaos/acervo/', AcervoView.as_view(), name='api-acervo'),
]
