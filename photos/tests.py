from django.core.urlresolvers import reverse
from django.template import Template, Context
from django.test import TestCase

from .admin import GalleryAdmin
from .models import Gallery, GalleryImage


class TestGalleries(TestCase):
    fixtures = ['photos.json']

    def setUp(self):
        self.gallery = Gallery.objects.get(id=1)
        self.galleryImage = GalleryImage.objects.latest('id')

    def test_list(self):
        """
        Test gallery list
        """
        response = self.client.get(reverse('gallery_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('object_list' in response.context)
        self.assertTemplateUsed('galleries/gallery_list.html')

    def test_gallery_detail(self):
        """
        Test for valid gallery detail.
        """
        response = self.client.get(reverse('gallery_detail', args=[self.gallery.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('object' in response.context)
        self.assertEquals(self.gallery.id, response.context['object'].id)
        self.assertTemplateUsed('galleries/gallery_detail.html')

    def test_gallery_model(self):
        self.assertTrue(self.gallery.has_image)
        self.assertEqual(self.gallery.get_image().url, self.galleryImage.image.url)
        self.gallery.galleryimage_set.all().delete()
        self.assertEquals(self.gallery.get_image(), None)

    def test_get_galleries_tag(self):
        "Test get galleries tag"
        out = Template(
            "{% load gallery_tags %}"
            "{% get_galleries 1 as galleries %}"
            "{% for gallery in galleries %}"
            "{{ gallery.title }}"
            "{% endfor %}"
        ).render(Context())
        self.assertEqual(out, self.gallery.title)

    def test_get_related_galleries_tag(self):
        """
        Test get related galleries.
        We have no related galleries in the json, so this should be short.
        """
        out = Template(
            "{% load gallery_tags %}"
            "{% get_related_galleries object 10 %}"
        ).render(Context({'object': self.gallery}))
        self.assertEqual(out, '\n')

    def test_admin_actions(self):
        gallery_actions = [action.short_description for action in GalleryAdmin.actions]
        self.assertTrue('Publish' in gallery_actions)
        self.assertTrue('Unpublish' in gallery_actions)
