import pandas

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from backtv_django import DAO
from .models import (
        list_orgaos_query,
        list_vistas_query,
        acervo_qtd_query,
        list_acervo_query,
        list_detalhes_query,
        acervo_classe_pai_query
        )


class OrgaosListView(APIView):
    def get(self, request, *args, **kwargs):
        data = DAO.run(list_orgaos_query)
        results = []
        for row in data:
            row_dict = {
                'cdorg': row[0],
                'craai': row[1],
                'comarca': row[2],
                'foro': row[3],
                'orgao': row[4],
                'titular': row[5],
            }
            results.append(row_dict)

        return Response(data=results)


class VistasListView(APIView):
    def get(self, request, *args, **kwargs):
        cdorg = request.GET.get('cdorg')
        results = []
        if cdorg is not None:
            data = DAO.run(list_vistas_query, {'org': cdorg})
            results = []
            for row in data:
                row_dict = {
                    'total': row[0],
                    'hoje': row[1],
                    'ate_30': row[2],
                    'de_30_a_40': row[3],
                    'mais_40': row[4],
                }
                results.append(row_dict)

        return Response(data=results)


class AcervoView(APIView):
    def get(self, request, *args, **kwargs):
        result = {"acervo_atual": [], 'historico': []}
        cdorg = request.GET.get('cdorg')
        if cdorg:
            acervo = DAO.run(acervo_qtd_query, {'org': cdorg}).fetchone()[0]
            result['acervo_atual'] = acervo
            meses = DAO.run(list_acervo_query, {'org': cdorg}).fetchall()

            historico = []
            prev_acervo = acervo
            for mes in meses:
                acervo_fim_mes = prev_acervo
                entradas = mes[1]
                saidas = mes[2]
                saldo = entradas - saidas
                acervo_inicio_mes = acervo_fim_mes - saldo  # Olhando para trás

                mes_dict = {
                    'mes': mes[0],
                    'entradas': entradas,
                    'saidas': saidas,
                    'acervo_fim_mes': acervo_fim_mes,
                    'saldo': saldo,
                    'acervo_inicio_mes': acervo_inicio_mes
                }

                historico.append(mes_dict)
                prev_acervo = acervo_inicio_mes

            result['historico'] = historico

        return Response(data=result)


class DetalhesView(APIView):
    def get(self, request, *args, **kwargs):
        cdorg = request.GET.get('cdorg')
        data = list(DAO.run(list_detalhes_query, {'org': cdorg}))

        colunas = """mmpm_ordem
                    mmpm_mapa_craai
                    mmpm_mapa_forum
                    mmpm_mapa_bairro
                    mmpm_mapa_municipio
                    mmpm_craai
                    mmpm_comarca
                    mmpm_foro
                    mmpm_grupo
                    mmpm_orgao
                    mmpm_telefonesorgao
                    mmpm_exibegrupo
                    mmpm_exibeforo
                    mmpm_ordemgrupo
                    mmpm_ordemquadro
                    mmpm_matricula
                    mmpm_nome
                    mmpm_celular
                    mmpm_cargo
                    mmpm_concurso
                    mmpm_anoconcurso
                    mmpm_romano
                    mmpm_funcao
                    mmpm_ordemsubstitucao
                    mmpm_flag_pgj
                    mmpm_flag_eleitoral
                    mmpm_flag_craai
                    mmpm_dias
                    mmpm_afastamento
                    mmpm_pgj_funcao
                    mmpm_dtnasc
                    mmpm_dtiniciosubs
                    mmpm_dtfimsubs
                    mmpm_flag_assessor
                    mmpm_cdorgao
                    """.split("\n")

        colunas = [c.strip() for c in colunas]
        data = [dict(zip(colunas, d)) for d in data]

        if not data:
            return Response(data={})

        retorno = {
                "detalhes": {
                    "matricula": data[0]["mmpm_matricula"],
                    "nome": data[0]["mmpm_nome"],
                    "cargo": data[0]["mmpm_cargo"],
                    "concurso": data[0]["mmpm_concurso"],
                    "anoconcurso": data[0]["mmpm_anoconcurso"],
                    "romano": data[0]["mmpm_romano"],
                    "flag_pgj": data[0]["mmpm_flag_pgj"],
                    "flag_eleitoral": data[0]["mmpm_flag_eleitoral"],
                    "flag_craai": data[0]["mmpm_flag_craai"],
                    "dtnasc": data[0]["mmpm_dtnasc"],
                    "flag_assessor": data[0]["mmpm_flag_assessor"],
                    "cdorgao": data[0]["mmpm_cdorgao"],
                    "telefonesorgao": data[0]["mmpm_telefonesorgao"].split(' | ')[1:],
                    "orgao": data[0]["mmpm_orgao"],
                    "celular": data[0]["mmpm_celular"],
                    },
                "funcoes": data[0]["mmpm_pgj_funcao"].split('@'),
                "designacoes": get_designacao(data[1:]),
                "afastamento": (data[0]["mmpm_afastamento"].split('@')
                    if data[0]["mmpm_afastamento"] else [])

        }
        return Response(data=retorno)


class AcervoClasseView(APIView):
    def get(self, request, *args, **kwargs):
        cdorg = request.GET.get('cdorg')
        data = DAO.run(acervo_classe_pai_query, {'org': cdorg})
        results = []
        if cdorg is not None:
            for row in data:
                row_dict = {
                    'classe_id_pai': row[0],
                    'classe_pai': row[1],
                    'qtd': row[2]
                }
                results.append(row_dict)

        return Response(data=results)


class FinanceiroView(APIView):
    def get(self, request, *args, **kwargs):
        cdorg = int(request.GET.get('cdorg'))
        consolidados = pandas.read_csv(
                'orgaos/sheets/consolidacao.csv', sep=';',
                converters={'Total': format_money,
                            'Área do Layout': to_float}
        )
        orgaos = pandas.read_csv('orgaos/sheets/orgaos.csv', sep=';')
        imoveis = pandas.read_csv('orgaos/sheets/imoveis.csv', sep=';')

        nome_promotoria = (
            orgaos[orgaos['Código do Órgão'] == cdorg]
            ['Nome do Órgão'].values
        )

        if nome_promotoria.size == 0:
            return Response(data={})

        df_orgao = (
            consolidados[consolidados['Centro de Custos'] == nome_promotoria[0]]
        )
        area_orgao = df_orgao['Área do Layout'].values[0]
        custo = df_orgao['Total'].sum()
        codigo_imovel = df_orgao['Código do Imóvel'].values[0]
        natureza = (
            imoveis[imoveis['CÓDIGO'] == codigo_imovel]['NATUREZA'].values[0]
        )

        return Response(data={
                'custo_orgao': custo,
                'area_orgao': area_orgao,
                'natureza': natureza
            })


class FinanceiroAgrupadoView(APIView):
    def get(self, request, *args, **kwargs):
        cdorg = int(request.GET.get('cdorg'))
        consolidados = pandas.read_csv(
                    'orgaos/sheets/consolidacao.csv', sep=';',
                    converters={'Total': format_money,
                                'Área do Layout': to_float}
        )
        orgaos = pandas.read_csv('orgaos/sheets/orgaos.csv', sep=';')

        if orgaos[orgaos['Código do Órgão'] == cdorg]['Nome do Órgão'] \
                .values.size == 0:
            return Response(data={})

        nome_promotoria = (
            orgaos[orgaos['Código do Órgão'] == cdorg]['Nome do Órgão'].values[0]
        )

        df_orgao = (
            consolidados[consolidados['Centro de Custos'] == nome_promotoria]
        )
        df_orgao['Tipo de Custo'] = df_orgao['Tipo de Custo'].str.lower()

        return Response(
            data=df_orgao.groupby('Tipo de Custo').Total.sum().to_dict()
        )


class UploadOrgaoSheetsView(APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, format=None):
        file_obj = request.FILES['file']
        with open('orgaos/sheets/orgaos.csv', 'wb') as out_put:
            out_put.write(file_obj.read())

        return Response(status=204)


class UploadImoveisSheetsView(APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, format=None):
        file_obj = request.FILES['file']
        with open('orgaos/sheets/imoveis.csv', 'wb') as out_put:
            out_put.write(file_obj.read())

        return Response(status=204)


class UploadConsolidacaoSheetsView(APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, format=None):
        file_obj = request.FILES['file']
        with open('orgaos/sheets/consolidacao.csv', 'wb') as out_put:
            out_put.write(file_obj.read())

        return Response(status=204)


def get_designacao(arr):
    return [
        {
            'mmpm_matricula': a['mmpm_matricula'],
            'mmpm_nome': a['mmpm_nome'],
            'mmpm_funcao': a['mmpm_funcao'],
            'mmpm_dtiniciosubs': a['mmpm_dtiniciosubs'],
            'mmpm_dtfimsubs': a['mmpm_dtfimsubs']
        }
        for a in arr
    ]


def to_float(val):
    try:
        return float(val.replace(',', '.'))
    except ValueError:
        return 0


def format_money(val):
    try:
        val = val.replace('R$', '').replace('.', '').replace(',', '.')
        return float(val)
    except ValueError:
        return 0
