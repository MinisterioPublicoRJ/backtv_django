from unittest import mock

from django.test import TestCase
from django.urls import reverse

from news.fixtures import ebc_fixture, valor_politico_fixtures, valor_brasil_fixture


class News(TestCase):
    @mock.patch('news.views.feedparser')
    def test_news_response(self, _feedparser):
        _feedparser.parse.side_effect = [
                ebc_fixture,
                valor_politico_fixtures,
                valor_brasil_fixture
        ]

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
        self.assertEqual(resp_json[0],
            {
             'source': 'Valor Econômico - Brasil',
             'title': 'mock_title_vb',
             'summary': 'mock_summary_vb',
             'href': 'mock_link_vb',
             'published': 'mock_published_vb',
             'published_parsed': 3
             }
        )
        self.assertEqual(resp_json[1],
            {
             'source': 'Empresa Brasil de Comunicação',
             'title': 'mock_title_ebc',
             'summary': 'mock_summary_ebc',
             'href': 'mock_link_ebc',
             'published': 'mock_published_ebc',
             'published_parsed': 2
             }
        )
        self.assertEqual(resp_json[2],
            {
            'source': 'Valor Econômico - Política',
            'title': 'mock_title_vp',
             'summary': 'mock_summary_vp',
             'href': 'mock_link_vp',
             'published': 'mock_published_vp',
             'published_parsed': 1
             }
        )
