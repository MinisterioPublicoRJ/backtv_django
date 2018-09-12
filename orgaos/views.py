from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
        run,
        list_orgaos_query,
        list_vistas_query,
        acervo_qtd_query,
        list_acervo_query
        )


class OrgaosListView(APIView):
    def get(self, request, *args, **kwargs):
        data = run(list_orgaos_query)
        results = []
        for row in data:
            row_dict = {
                'CDORG': row[0],
                'CRAAI': row[1],
                'COMARCA': row[2],
                'FORO': row[3],
                'ORGAO': row[4],
                'TITULAR': row[5],
            }
            results.append(row_dict)

        return Response(data=results)


class VistasListView(APIView):
    def get(self, request, *args, **kwargs):
        cdorg = request.GET.get('cdorg')
        results = []
        if cdorg is not None:
            data = run(list_vistas_query, {'org': cdorg})
            results = []
            for row in data:
                row_dict = {
                    'TOTAL': row[0],
                    'HOJE': row[1],
                    'ATE_30': row[2],
                    'DE_30_A_40': row[3],
                    'MAIS_40': row[4],
                }
                results.append(row_dict)

        return Response(data=results)


class AcervoView(APIView):
    def get(self, request, *args, **kwargs):
        result = {"ACERVO_ATUAL": [], 'HISTORICO': []}
        cdorg = request.GET.get('cdorg')
        if cdorg:
            acervo = run(acervo_qtd_query, {'org': cdorg}).fetchone()[0]
            result['ACERVO_ATUAL'] = acervo
            meses = run(list_acervo_query, {'org': cdorg}).fetchall()

            historico = []
            prev_acervo = acervo
            for mes in meses:
                acervo_fim_mes = prev_acervo
                entradas = mes[1]
                saidas = mes[2]
                saldo = entradas - saidas
                acervo_inicio_mes = acervo_fim_mes - saldo  # Olhando para trás

                mes_dict = {
                    'MES': mes[0],
                    'ENTRADAS': entradas,
                    'SAIDAS': saidas,
                    'ACERVO_FIM_MES': acervo_fim_mes,
                    'SALDO': saldo,
                    'ACERVO_INICIO_MES': acervo_inicio_mes
                }

                historico.append(mes_dict)
                prev_acervo = acervo_inicio_mes

            result['HISTORICO'] = historico

        return Response(data=result)
