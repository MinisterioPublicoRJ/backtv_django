from unittest import mock

from django.test import TestCase
from django.urls import reverse


class Orgaos(TestCase):
    @mock.patch('orgaos.views.run')
    def test_list_orgaos(self, _run):
        url = reverse('orgaos:api-list-orgaos')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    @mock.patch('orgaos.views.run')
    def test_list_vistas(self, _run):
        url = reverse('orgaos:api-list-vistas')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    @mock.patch('orgaos.views.run')
    def test_acervo(self, _run):
        url = reverse('orgaos:api-acervo')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
