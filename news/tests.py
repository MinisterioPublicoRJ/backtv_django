from unittest import mock

from django.test import TestCase
from django.urls import reverse

from news.fixtures import ebc_fixture, valor_politico_fixtures, valor_brasil_fixture


class News(TestCase):
    @mock.patch('news.views.feedparser')
    def test_news_response(self, _feedparser):
        _feedparser.side_effect = [ebc_fixture, valor_politico_fixtures, valor_brasil_fixture]

        url = reverse('news:api-news')
        resp = self.client.get(url)

        resp_json = resp.json()

        _feedparser_calls = [
            mock.call('http://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml'),
            mock.call('https://www.valor.com.br/politica/rss'),
            mock.call('https://www.valor.com.br/brasil/rss')
        ]

        self.assertEqual(resp.status_code, 200)
        _feedparser.parse.assert_has_calls(_feedparser_calls)
        self.assertEqual(resp_json, )
