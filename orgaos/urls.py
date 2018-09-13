from django.urls import path

from orgaos.views import (
        OrgaosListView,
        VistasListView,
        AcervoView,
        DetalhesView,
        AcervoClasseView,
        FinanceiroView,
        FinanceiroAgrupadoView,
        UploadOrgaoSheetsView,
        UploadImoveisSheetsView,
        UploadConsolidacaoSheetsView
        )


app_name = 'orgaos'
urlpatterns = [
    path('orgaos/', OrgaosListView.as_view(), name='api-list-orgaos'),
    path('orgaos/vistas/', VistasListView.as_view(), name='api-list-vistas'),
    path('orgaos/acervo/', AcervoView.as_view(), name='api-acervo'),
    path('orgaos/detalhes/', DetalhesView.as_view(), name='api-detalhes'),
    path('orgaos/acervo-classe/',
         AcervoClasseView.as_view(),
         name='api-acervo-classe'),
    path('orgaos/financeiro/',
         FinanceiroView.as_view(),
         name='api-financeiro'),
    path(
        'orgaos/financeiro/agrupado/',
        FinanceiroAgrupadoView.as_view(), name='api-financeiro-agrupado'
    ),
    path('orgaos/upload/orgaos',
         UploadOrgaoSheetsView.as_view(), name='upload-sheets-orgaos'),
    path('orgaos/upload/imoveis',
         UploadImoveisSheetsView.as_view(), name='upload-sheets-imoveis'),
    path('orgaos/upload/consolidacao',
         UploadConsolidacaoSheetsView.as_view(),
         name='upload-sheets-consolidacao'),
]
