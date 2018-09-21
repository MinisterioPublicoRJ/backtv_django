import re

from operator import itemgetter

import feedparser

from rest_framework.response import Response
from rest_framework.views import APIView


class NewsView(APIView):
    def get(self, request, *args, **kwargs):
        news = read_rss()
        return Response(data=news)


def read_rss():
    ebc = feedparser.parse(
        'http://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml'
    )
    valor_politico = feedparser.parse(
        'https://www.valor.com.br/politica/rss'
    )
    valor_brasil = feedparser.parse(
        'https://www.valor.com.br/brasil/rss'
    )

    news = []
    news.extend(iter_entries(ebc, source='Empresa Brasil de Comunicação'))
    news.extend(iter_entries(valor_politico,
                             source='Valor Econômico - Política'))
    news.extend(iter_entries(valor_brasil, source='Valor Econômico - Brasil'))

    return sorted(news, key=itemgetter('published_parsed'), reverse=True)


def iter_entries(entries, source):
    news = []
    for entry in entries['entries']:
        news.append(
                {
                'source': source,
                'title': entry['title'],
                'summary': remove_tags_html(entry['summary']),
                'href': entry['links'][0]['href'],
                'published': entry['published'],
                'published_parsed': entry['published_parsed']
                }
        )

    return news


def remove_tags_html(summary):
    pat = re.compile(r'<.*?>')
    return pat.sub('', summary)
