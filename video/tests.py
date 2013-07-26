from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Video


class TestVideo(TestCase):

    def test_youtube_video(self):
        """
        Test that newly saved youtube videos
        are correctly capturing values from youtube.
        """
        url = 'https://www.youtube.com/watch?v=c-wXZ5-Yxuc'
        test_video = Video(url=url)
        test_video.save()
        self.assertIsInstance(test_video, Video)
        self.assertEqual(test_video.source, 'youtube')

        video_dict = test_video.__dict__
        self.assertIn('title', video_dict)
        self.assertIn('slug', video_dict)
        self.assertIn('description', video_dict)
        self.assertIn('thumb_url', video_dict)

        response = self.client.get(reverse('video_detail', args=[test_video.slug, ]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('video_detail.html')
        self.assertIn('object', response.context)
        object = response.context['object']
        self.assertIsInstance(object, Video)

    def test_vimeo_video(self):
        """
        Test that newly saved vimeo videos
        are correctly capturing values from youtube.
        """
        url = 'http://vimeo.com/67325705'
        test_video = Video(url=url)
        test_video.save()
        self.assertIsInstance(test_video, Video)
        self.assertEqual(test_video.source, 'vimeo')
        self.assertTrue('Tango' in test_video.title)

        video_dict = test_video.__dict__
        self.assertIn('title', video_dict)
        self.assertIn('slug', video_dict)
        self.assertIn('description', video_dict)
        self.assertIn('thumb_url', video_dict)

        response = self.client.get(reverse('video_detail', args=[test_video.slug, ]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('video_detail.html')
        self.assertIn('object', response.context)
        object = response.context['object']
        self.assertIsInstance(object, Video)


