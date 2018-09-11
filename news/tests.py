from django.test import TestCase
from django.urls import reverse


class News(TestCase):
    def test_news_response(self):
        url = reverse('news:api-news')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)