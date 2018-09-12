from rest_framework.response import Response
from rest_framework.views import APIView

from .model import run, list_orgaos_query


class OrgaosView(APIView):
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
