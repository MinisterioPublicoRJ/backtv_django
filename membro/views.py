import base64

from rest_framework.response import Response
from rest_framework.views import APIView

from backtv_django import DAO
from .models import foto_mat_query


class MembroFotoView(APIView):
    def get(self, request, *args, **kwargs):
        cdmat = request.GET.get('cdmat')
        results = []
        if cdmat is not None:
            data = DAO.run(foto_mat_query, {'mat': cdmat})
            for row in data:
                row_dict = {
                    'foto': base64.b64encode(row[0].read()).decode()
                }
                results.append(row_dict)

        return Response(data=results)
