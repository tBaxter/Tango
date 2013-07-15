from django import forms
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core import mail
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404

UserModel = get_user_model()


class ContactForm(forms.Form):
    name = forms.CharField()
    from_address = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


def contact(request, slug=""):
    site = Site.objects.get_current()
    user = request.user
    if slug:
        recipient = get_object_or_404(UserModel, username=slug)
        try:
            recipient_name = recipient.preferred_name
        except:
            raise Http404
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            if slug == "":  # staff contact form
                to = 'baxter@gretschpages.com'
            else:  # member contact form
                to = recipient.email
            mail.send_mail(
                "A " + site.domain + " message from " + form.cleaned_data['name'],
                form.cleaned_data['message'],
                form.cleaned_data['from_address'],
                [to],
                fail_silently = False
            )
            return HttpResponseRedirect('/contact/done/')
    else:
        form = ContactForm()
    if slug:
        return render(request, 'users/user-contact-form.html', {'form': form, 'recipient_name': recipient_name, 'user': user, 'site': site})
    return render(request, 'contact/form.html', {'form': form, 'user': user, 'site': site},)
