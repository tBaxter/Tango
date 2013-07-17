from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
    """
    Base contact form
    """
    required_css_class = 'required'

    class Meta:
        model = Contact
        fields = ['sender_name', 'sender_email', 'body', 'send_a_copy']

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['sender_name'].label = "Your name"
        self.fields['sender_email'].label = "Your e-mail address"
        self.fields['body'].label = "Your message"
