from django.test import TestCase
from django.urls import reverse


class Clima(TestCase):
    def test_clima_response(self):
        url = reverse('clima:api-clima')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
