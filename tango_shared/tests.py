from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase


class TestSharedContent(TestCase):

    def setUp(self):
        self.slug    = 'admin'

    def test_template_media(self):
        """
        Ensures base template has required media files.
        """
        response = self.client.get(reverse('home'))
        favicon_url = '<link rel="shortcut icon" href="%simg/favicon.png">' % settings.STATIC_URL
        touch_icon = '<link rel="apple-touch-icon" href="%simg/touch-icon.png">' % settings.STATIC_URL
        self.assertEqual(response.status_code, 200)
        self.assertTrue(favicon_url in response.content)
        self.assertTrue(touch_icon in response.content)

    def test_shared_context_processor(self):
        """
        Test results of shared context processor are in template
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('site' in response.context)
        self.assertTrue('now' in response.context)
        self.assertTrue('year' in response.context)
        self.assertTrue('ga_code' in response.context)
        self.assertTrue('project_name' in response.context)
        self.assertTrue('current_path' in response.context)
        self.assertTrue('last_seen' in response.context)
        self.assertTrue('last_seen_fuzzy' in response.context)
        self.assertTrue('theme' in response.context)
        self.assertTrue('authenticated_request' in response.context)
