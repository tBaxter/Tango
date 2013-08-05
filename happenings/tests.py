from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Event


class TestHappeningsGeneralViews(TestCase):
    fixtures = ['events.json']

    def setUp(self):
        self.event = Event.objects.get(id=1)

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

