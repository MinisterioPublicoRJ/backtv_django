import responses

from django.test import TestCase
from django.urls import reverse

from clima.views import URL


class Clima(TestCase):
    @responses.activate
    def test_clima_response(self):
        metar_resp = '2018/09/04 17:00\nSBRJ 041700Z 21013KT 9999 SCT030 26/13 Q1009'
        responses.add(
            responses.GET,
            URL,
            body=metar_resp
        )

        url = reverse('clima:api-clima')
        resp = self.client.get(url)

        resp_json = resp.json()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_json['temperature'], '26.0')
