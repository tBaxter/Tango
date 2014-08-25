import datetime

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.template import Template, Context
from django.test import TestCase

UserModel = get_user_model()

today = datetime.date.today()


class TestUserProfileViews(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.user = UserModel.objects.get(id=1)

    def test_index(self):
        """
        Test community index
        """
        response = self.client.get(reverse('community_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('object_list' in response.context)
        self.assertTemplateUsed("users/user_list.html")
        response = self.client.get(reverse('community_index') + '?state=ks')
        self.assertTrue('filter' in response.context)

    def test_detail(self):
        response = self.client.get(reverse('view_profile', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('user' in response.context)
        response_user = response.context['user']
        self.assertEqual(response_user.id, self.user.id)
        self.assertEqual(response_user.username, self.user.username)
        self.assertEqual(response_user.get_display_name(), self.user.username)

    def test_edit_profile(self):
        """
        Test edit profile form
        """
        self.client.login(username=self.user.username, password='test')
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('object' in response.context)
        self.assertTrue('form' in response.context)
        self.assertTemplateUsed("users/user_edit_form.html")

    def test_edit_settings(self):
        self.client.login(username=self.user.username, password='test')
        response = self.client.get(reverse('edit_settings'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('object' in response.context)
        self.assertTrue('form' in response.context)
        self.assertTemplateUsed("users/user_edit_form.html")

    def test_birthdays_tag(self):
        """
        Test birthdays
        """
        out = Template(
            "{% load user_tags %}"
            "{% get_birthday_list as birthday_list %}"
            "{% for bday in birthday_list %}"
            "{{ user.username }},"
            "{% endfor %}"
        ).render(Context())
        todays_birthdays = ','.join(UserModel.objects.filter(birthday__month = today.month, birthday__day = today.day).values_list('username', flat=True))
        self.assertEqual(out, todays_birthdays)

    def test_new_members_tag(self):
        """
        Test new members list.
        Since there are no new members in the JSON, this should return nothing.
        """
        # test by count
        out = Template(
            "{% load user_tags %}"
            "{% get_new_members 5 as new_members %}"
            "{% for member in new_members %}"
            "{{ user.username }}"
            "{% endfor %}"
        ).render(Context())
        self.assertEqual(out, '')

        # test for today
        out = Template(
            "{% load user_tags %}"
            "{% get_new_members 'today' as new_members %}"
            "{% for member in new_members %}"
            "{{ user.username }}"
            "{% endfor %}"
        ).render(Context())
        self.assertEqual(out, '')
