from django import forms

from .models import Blacklist


class BlacklistForm(forms.ModelForm):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

    class Meta:
        model = Blacklist
