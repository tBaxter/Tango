from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Article


class TestArticleViews(TestCase):
    fixtures = ['users.json', 'articles.json']

    def test_settings(self):
        paginate_by = getattr(settings, "PAGINATE_BY", False)
        self.assertTrue(paginate_by, "settings.PAGINATE_BY does not exist. You should create it.")

    def test_article_detail(self):
        """
        Test article detail
        """
        article = Article.objects.get(id=1)
        response = self.client.get(reverse('article_detail', args=[article.slug, ]))
        self.assertEqual(response.status_code, 200)

        self.assertIn('object', response.context)
        obj = response.context['object']
        self.assertIsInstance(obj, Article)

    def test_article_list(self):
        """
        Test article list
        """
        response = self.client.get(reverse('article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('object_list' in response.context)
