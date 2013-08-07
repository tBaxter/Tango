from django.core.urlresolvers import reverse
from django.template import Template, Context
from django.test import TestCase

from .models import Video, VideoGallery
from .forms import VideoForm


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
        self.assertIn('summary', video_dict)
        self.assertIn('thumb_url', video_dict)

        response = self.client.get(reverse('video_detail', args=[test_video.slug, ]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('video_detail.html')
        self.assertIn('object', response.context)
        object = response.context['object']
        self.assertIsInstance(object, Video)
        self.assertTrue(hasattr(object, 'title'))
        self.assertTrue(hasattr(object, 'summary'))
        self.assertTrue(hasattr(object, 'embed_src'))

        # test template Tag:
        out = Template(
            "{% load video_tags %}"
            "{% show_video object %}"
        ).render(Context({'object': object}))
        self.assertIn(object.title, out)
        self.assertIn(object.embed_src, out)

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
        self.assertIn('summary', video_dict)
        self.assertIn('thumb_url', video_dict)

        response = self.client.get(reverse('video_detail', args=[test_video.slug, ]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('video_detail.html')
        self.assertIn('object', response.context)
        object = response.context['object']
        self.assertIsInstance(object, Video)

    def test_recent_video_tag(self):
        out = Template(
            "{% load video_tags %}"
            "{% get_video_list as video_list %}"
            "{% for video in video_list %}"
            "{{ video.title }},"
            "{% endfor %}"
        ).render(Context())
        self.assertEqual(out, '')

    def test_video_form(self):
        fields = VideoForm().fields
        self.assertFalse(fields['title'].required)
        self.assertFalse(fields['slug'].required)
        self.assertFalse(fields['summary'].required)

    def test_video_gallery_detail(self):
        gallery = VideoGallery.objects.create(title= 'test gallery', slug='test-gallery')
        response = self.client.get(reverse('video_gallery_detail', args=[gallery.slug, ]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('object', response.context)
        self.assertIn('gallery', response.context)
        self.assertTemplateUsed('video/video_list.html')

        #ensure we also attempted to pass a video list
        self.assertIn('object_list', response.context)
