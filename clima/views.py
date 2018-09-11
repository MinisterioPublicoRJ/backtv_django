from django.http import JsonResponse
from django.views.generic import View


class ClimaView(View):
    def get(self, request, format=None):
        return JsonResponse(data={})
