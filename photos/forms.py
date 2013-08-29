from django import forms

from .models import Gallery, supports_articles


class GalleryForm(forms.ModelForm):
    """
    Base form for gallery uploads
    """
    bulk_upload = forms.FileField(
        widget=forms.FileInput(attrs={'multiple': 'multiple'}),
        required=False
    )

    class Meta:
        model = Gallery
        # to do: append article to fields rather than re-declare
        fields = ['overline', 'title', 'slug', 'credit', 'summary', 'published', 'bulk_upload']
        if supports_articles:
            fields = ['overline', 'title', 'slug', 'credit', 'summary', 'published', 'article', 'bulk_upload']
