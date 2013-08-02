from django import forms

from .models import BulkImageUpload, Gallery, GalleryImage


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
        fields = ['overline', 'title', 'slug', 'credit', 'summary', 'published', 'article', 'bulk_upload']

    #def save(self, force_insert=False, force_update=False, commit=True):
    #    super(GalleryForm, self).save()


class BulkUploadForm(forms.ModelForm):
    """ This form is only used to handle the uploads """
    class Meta:
        model = BulkImageUpload
        widgets = {
            'files':   forms.FileInput(attrs={'multiple': 'multiple'}),
        }

    def save(self, force_insert=False, force_update=False, commit=True):
        upload_form = super(BulkUploadForm, self).save(commit=False)
        print upload_form.data['files'].get
    #    print 'request'
    #    print self.cleaned_data['files']
    #    #print 'uploads'
    #    #print uploads
    #    #for f in uploads:
    #        #print type(f)
    #        #new_image = GalleryImage(
    #        #    gallery         = self.instance,
    #        #    image           = f,
    #            #caption         = self.instance.caption,
    #        #)
    #        #new_image.save()
    #        #print new_image
    #    #self.fields.pop('bulk_upload')

