import time

from django import forms

from .models import BulkImageUpload, Gallery, GalleryImage


class GalleryForm(forms.ModelForm):
    """
    Base form for gallery uploads
    """
    class Meta:
        model = Gallery


class BulkUploadForm(forms.ModelForm):
    class Meta:
        model = BulkImageUpload
        widgets = {
            'files':   forms.FileInput(attrs={'multiple': 'multiple'}),
        }

