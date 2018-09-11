import feedparser

from django.http import JsonResponse
from django.views.generic import View


class NewsView(View):
    def get(self, request, *args, **kwargs):
        news = read_rss()
        return JsonResponse(data=news, safe=False)


def read_rss():
    ebc = feedparser.parse(
        'http://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml'
    )
    valor_politica = feedparser.parse(
        'https://www.valor.com.br/politica/rss'
    )
    valor_brasil = feedparser.parse(
        'https://www.valor.com.br/brasil/rss'
    )

    return [{'data': 1}]
