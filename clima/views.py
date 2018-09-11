import requests

from django.http import JsonResponse
from django.views.generic import View
from metar import Metar

URL = "http://tgftp.nws.noaa.gov/data/observations/metar/stations/SBRJ.TXT"


class ClimaView(View):
    def get(self, request, *args, **kwargs):
        resp_content = requests.get(URL).content.decode('UTF-8')
        metar_obj = Metar.Metar('METAR ' + resp_content.split('\n')[1])
        temperature = str(metar_obj.temp).split(' ')[0]
        return JsonResponse(data={'temperature': temperature})
