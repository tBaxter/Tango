from django.core.urlresolvers import reverse
from django.test import TestCase



class TestContactViews(TestCase):

    def setUp(self):
        self.slug    = 'admin'

    def test_member_contact(self):
        """
        Test member contact form
        """
        resp = self.client.get(reverse('contact_member', args=[self.slug]))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('form' in resp.context)
        self.assertTrue('user' in resp.context)
        self.assertTrue('site' in resp.context)

    def test_admin_contact(self):
        """
        Test site admin contact form
        """
        resp = self.client.get(reverse('contact_site'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('form' in resp.context)
        self.assertTrue('user' in resp.context)
        self.assertTrue('site' in resp.context)
        self.assertTrue(resp.context['user'].is_superuser == 1)
