from django import forms

from .models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'summary', 'url', 'video_at_top', 'hide_info',]

    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        self.fields['title'].help_text = "We'll attempt to fill this in from the video service."
        self.fields['title'].required = False
        self.fields['slug'].required = False
        self.fields['summary'].help_text = "We'll attempt to fill this in from the video service."
        self.fields['summary'].required = False
