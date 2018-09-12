from django.test import TestCase
from django.urls import reverse


class Orgaos(TestCase):
    def test_list_orgaos(self):
        url = reverse('orgaos:api-list-orgaos')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code,200)
