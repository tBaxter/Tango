from django import forms
from django.forms import ModelForm, HiddenInput, TextInput

from .models import Event, GiveawayResponse, PlaylistItem, Memory


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            'name', 'info',
            'start_date', 'end_date',
            'region', 'venue', 'city', 'state', 'zipcode', 'website'
        ]
        widgets = {
            'start_date':   TextInput(attrs={'class': 'datepicker'}),
            'end_date':     TextInput(attrs={'class': 'datepicker'}),
        }


class AddEventForm(EventForm):
    def clean(self):
        """
        Validate that an event with this name on this date does not exist.
        """
        cleaned_data = super(EventForm, self).clean()
        if Event.objects.filter(name=cleaned_data['name'], start_date=cleaned_data['start_date']).count():
            raise forms.ValidationError(u'This event appears to be in the database already.')
        return cleaned_data


class EventUpdateForm(EventForm):
    def clean_name(self):
        return self.cleaned_data['name']


class EventRecapForm(EventUpdateForm):
    class Meta(EventUpdateForm.Meta):
        fields = EventUpdateForm.Meta.fields.append('recap')


class GiveawayResponseForm(ModelForm):
    class Meta:
        model = GiveawayResponse
        exclude = ('closed', 'notes')
        widgets = {
            'respondent': HiddenInput(),
            'correct': HiddenInput(),
            'question': HiddenInput(),
        }


class PlayListForm(ModelForm):
    class Meta:
        model = PlaylistItem
        fields = ('title', 'link')
        widgets = {
            'event': HiddenInput(),
            'user': HiddenInput(),
        }


class MemoryForm(ModelForm):
    upload = forms.FileField(
        required=False,
        label = "Or upload your photos(s)",
        help_text='<span class="meta">You can upload one or several JPG files. Be kind, this isn\'t photobucket"</span>',
        widget=forms.FileInput(attrs={'multiple': 'multiple'})
    )
    upload_caption = forms.CharField(
        label="Caption",
        required=False,
        help_text="Note: if you are uploading multiple photos, one caption will be used.",
        widget=forms.TextInput()
    )

    def clean_upload(self):
        data = self.cleaned_data['upload']
        upload_name = data.name.lower()
        if not any(upload_name.endswith(x) for x in ('.jpg', '.jpeg', '.zip')):
            raise forms.ValidationError("Your upload must be in JPG or ZIP formats.")
        return data

    class Meta:
        model = Memory
        widgets = {
            'photos': HiddenInput()
        }
