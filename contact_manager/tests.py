from django.core.urlresolvers import reverse
from django.test import TestCase


class TestContactViews(TestCase):

    def test_admin_contact(self):
        """
        Test simple site admin contact form
        """
        response = self.client.get(reverse('simple_contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue('site' in response.context)

    def test_member_contact(self):
        """
        Test simple member contact form
        """
        response = self.client.get(reverse('member_contact_form', args=['monkey']))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue('site' in response.context)

    def test_contact_list(self):
        """
        Test contact_list_messages
        """
        response = self.client.get(reverse('contact_list'))
        self.assertEqual(response.status_code, 200)

    def test_contact_detail(self):
        """
        Test contact_detail
        """
        response = self.client.get(reverse('contact_detail'), args=[1])
        self.assertEqual(response.status_code, 200)

    def test_contact_builder(self):
        """
        Test contact_form_builder
        """
        response = self.client.get(reverse('build_contact'), args=['not-a-valid-controller-slug'])
        self.assertEqual(response.status_code, 404)
