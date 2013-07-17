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
        response = self.client.get("/")
        favicon_url = '<link rel="shortcut icon" href="%simg/favicon.png">' % settings.STATIC_URL
        touch_icon = '<link rel="apple-touch-icon" href="%simg/touch-icon.png">' % settings.STATIC_URL
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(favicon_url in resp.content)
        self.assertTrue(touch_icon in resp.content)

    def test_shared_context_processor(self):
        """
        Test results of shared context processor are in template
        """
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('site' in resp.context)
        self.assertTrue('now' in resp.context)
        self.assertTrue('year' in resp.context)
        self.assertTrue('ga_code' in resp.context)
        self.assertTrue('project_name' in resp.context)
        self.assertTrue('current_path' in resp.context)
        self.assertTrue('last_seen' in resp.context)
        self.assertTrue('last_seen_fuzzy' in resp.context)
        self.assertTrue('theme' in resp.context)
        self.assertTrue('authenticated_request' in resp.context)
