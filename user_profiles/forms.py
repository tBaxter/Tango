from django import forms

from .models import Profile


class PublicProfileForm(forms.ModelForm):
    """
    Allows for profile and settings updates.
    Note that template checks for "Open board links" label.
    Anything below that will be in a 'settings' fieldset.
    """
    class Meta:
        model = Profile
        fields = (
            'display_name',
            'street_address',
            'city',
            'state',
            'country',
            'zipcode',
            'occupation',
            'interests',
            'birthday',
            'homepage',
            'bio',
            'avatar',
            'signature',
        )


class ProfileSettingsForm(forms.ModelForm):
    """
    Allows for modifying profile settings
    """
    class Meta:
        model = Profile
        fields = (
            'display_on_map',
            'show_signatures',
            'theme'
        )
