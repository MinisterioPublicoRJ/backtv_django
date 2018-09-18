from unittest import mock

from django.test import TestCase
from django.urls import reverse


class Membro(TestCase):
    @mock.patch('membro.views.run')
    def test_get_photo(self, _run):
        url = reverse('membro:api-foto')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
