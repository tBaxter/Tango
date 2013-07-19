
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import ContactFormController, Contact

UserModel = get_user_model()


class TestContactViews(TestCase):
    fixtures = ['users.json', 'contact_form.json']

    def setUp(self):
        self.username = UserModel.objects.all()[0].username

    def test_admin_contact(self):
        """
        Test simple site admin contact form
        """
        response = self.client.get(reverse('simple_contact_form'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue('site' in response.context)

    def test_member_contact(self):
        """
        Test simple member contact form
        """
        response = self.client.get(reverse('member_contact_form', args=['invalid-username']))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('member_contact_form', args=[self.username]))
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
        response = self.client.get(reverse('contact_detail', args=[99999999999999]))
        self.assertEqual(response.status_code, 404)
        contact = Contact.objects.get(id=1)
        response = self.client.get(reverse('contact_detail', args=[contact.id]))
        self.assertEqual(response.status_code, 200)

    def test_contact_builder(self):
        """
        Test contact_form_builder
        """
        response = self.client.get(reverse('contact_form_builder', args=['not-a-valid-controller-slug', ]))
        self.assertEqual(response.status_code, 404)
        contact_form_slug = ContactFormController.objects.get(id=1).slug
        response = self.client.get(reverse('contact_form_builder', args=[contact_form_slug, ]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue('site' in response.context)