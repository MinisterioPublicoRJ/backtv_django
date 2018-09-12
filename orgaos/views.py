from rest_framework.response import Response
from rest_framework.views import APIView

from .models import run, list_orgaos_query, list_vistas_query


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
