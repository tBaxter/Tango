from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Event

UserModel = get_user_model()


class TestHappeningsGeneralViews(TestCase):
    fixtures = ['events.json', 'users.json']

    def setUp(self):
        self.event = Event.objects.get(id=1)
        self.user = UserModel.objects.all()[0]

    def test_index(self):
        """
        Test index
        """
        resp = self.client.get(reverse('events_index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('object_list' in resp.context)

    def test_events_by_region(self):
        """
        Test events_by_region
        """
        resp = self.client.get(reverse('events_by_region', args=['Pacific']))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('object_list' in resp.context)
        self.assertTrue('region' in resp.context)

    def test_event_detail(self):
        """
        Test for valid event detail.
        """
        resp = self.client.get(reverse('event_detail', args=[self.event.slug]))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('object' in resp.context)
        self.assertTrue('key' in resp.context)
        self.assertEquals(self.event.id, resp.context['object'].id)

        if self.event.ended:
            self.assertFalse('schedule/">Schedule</a>' in resp.content)

    def test_event_creation(self):
        """
        Test for valid event creation.
        """
        self.client.login(username=self.user.username, password='test')
        response = self.client.get(reverse('add_event'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        new_event = {
            "featured": True,
            "has_playlist": False,
            "submitted_by": 1,
            "add_date": "2013-08-05",
            "slug": "new-test-event",
            "start_date": "2013-08-10",
            "approved": True,
            "info": "This is a new test event.",
            "name": "New Test Event",
            "region": "Pacific",
        }
        response = self.client.post(reverse('add_event'))
        self.assertEqual(response.status_code, 200)

    def test_event_editing(self):
        """
        Test for valid event editing.
        """
        response = self.client.get(reverse('edit-event', args=[self.event.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('object' in response.context)
        self.assertTrue('form' in response.context)

    def test_ical_creation(self):
        response = self.client.get(reverse('event_ical', args=[self.event.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Type'].startswith('text/calendar'))
        self.assertEquals(response['Filename'], 'filename.ics')
        self.assertEquals(response['Content-Disposition'], 'attachment; filename=filename.ics')
        response_list = response.content.split('\r\n')
        self.assertEquals(response_list[0], 'BEGIN:VCALENDAR')
        self.assertEquals(response_list[9], 'SUMMARY:Test Event')
