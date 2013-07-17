from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView

from .forms import ContactForm
from .models import Contact

UserModel = get_user_model()
success_url = reverse('contact_done')


class ContactList(ListView):
    """
    Returns list of all stored messages.
    Messages are paginated according to settings.PAGINATE_BY.
    """
    template_name = 'contact/message_list.html'
    paginate_by = settings.PAGINATE_BY
    queryset = Contact.objects.filter(publish=True, site__id=settings.SITE_ID).order_by('-id')
contact_list = ContactList.as_view()


class FormContacts(ContactList):
    """
    Returns all stored comments/messages for a given
    contact form controller.
    """
    def dispatch(self, request, *args, **kwargs):
        self.controller_slug = kwargs.get('controller_slug', False)
        return super(FormContacts, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(FormContacts, self).get_queryset()
        return queryset.filter(controller__slug=self.controller_slug)
form_comments_list = FormContacts.as_view()


class ContactDone(TemplateView):
    """
    Returns simple thank you page after comment submission.
    """
    template_name = 'contact/done.html'
contact_done = ContactDone.as_view()


class ContactDetail(DetailView):
    """
    Simple contact detail view.
    """
    model = Contact
contact_detail = ContactDetail.as_view()


def simple_contact(request, username=""):
    """
    Defines simple contact form that can be used to
    contact a site member passed by username in the URL
    or to all site admins.
    """
    site = Site.objects.get_current()
    form = ContactForm(request.POST or None)
    if username:
        recipients = get_object_or_404(UserModel, username=username)
        recipients = list(recipients.email)
    else:  # site contact form. Use settings.ADMIN
        recipients = [admin[1] for admin in settings.ADMIN]
    if form.is_valid():
        subject = "A " + site.domain + " message from " + form.cleaned_data['sender_name']
        mail = EmailMessage(
            subject,
            form.cleaned_data['body'],
            form.cleaned_data['from_address'],
            recipients,
            fail_silently = False
        )
        mail.send()
        if 'send_a_copy' in form.cleaned_data:
            mail = EmailMessage(
                subject = subject,
                body = form.cleaned_data['body'],
                from_email = form.cleaned_data['sender_email'],
                to = form.cleaned_data['sender_email']
            )
            mail.send()
        return HttpResponseRedirect(success_url)
    return render(request, 'contact/form.html', {
        'form': form,
        'site': site
    })


def build_contact(request, slug="", return_form=False, content_obj=None):
    """
    Builds appropriate contact form based on options
    set in the contact_form controller.
    """
    controller = get_object_or_404(ContactForm, slug=slug)
    site = Site.objects.get_current()
    user = request.user

    # Instantiate the form so we don't clutter the global one
    form = ContactForm(request.POST or None, request.FILES or None)

    if controller.send_emails:
        # build recipient_list from staff recipients and other recipients
        to_choices = [(r.username, r.get_fullname()) for r in controller.recipients.all()]
        for r in controller.other_recipients.all():
            to_choices.append((r.name, r.email))
        # if 'Create selectable list of recipients' is selected, add to form
        if controller.email_options == '2':
            form.fields.insert('to', 0)
            form.fields['to'] = forms.ChoiceField(choices=to_choices)

    if controller.ask_for_subject:
        form.fields.insert(0, 'subject')
        if controller.subject_label:  # we're overriding the subject label
            form.fields['subject'].label = controller.subject_label

    if controller.body_label:  # we're overriding the body label
        form.fields['body'].label = controller.body_label

    # if we know, fill in the user name and email
    if user.is_authenticated():
        form.fields['sender_name'].widget.attrs['disabled'] = 'disabled'
        form.fields['sender_email'].widget.attrs['disabled'] = 'disabled'
        form(initial={
            'sender_name': user.username,
            'sender_email': user.email,
        })

    # if we want contact info
    if controller.request_contact_info:
        form.fields.extend(['contact_address', 'contact_city', 'contact_state', 'contact_phone', ])
        form.fields['contact_address'].required = True
        form.fields['contact_city'].required = True
        form.fields['contact_state'].required = True
        form.fields['contact_phone'].required = True

    # If there's a file
    if controller.allow_uploads:
        form.fields.append('photo')

    if form.is_valid():
        if controller.store_in_db:
            new_msg = form.save(commit=False)
            new_msg.controller = controller
            new_msg.site = site
            if controller.override_subject:  # we're overriding the subject
                new_msg.subject = controller.override_subject
            new_msg.save()

        # if we're sending emails
        form_data = form.cleaned_data
        if controller.override_subject:
            subject = controller.override_subject
        elif 'subject' in form_data:
            subject = form_data['subject']
        else:
            subject = "%s message from %s" % (controller.name, form_data['sender_name'])

        body = "%s \n\n %s" % (form_data['body'], form_data['sender_name'])
        if controller.request_contact_info:
            body += "\nAddress: %s \nCity: %s \nState: %s \nPhone: %s" % (
                form_data['contact_address'],
                form_data['contact_city'],
                form_data['contact_state'],
                form_data['contact_phone']
            )

        if controller.email_options == '2':  # Create selectable list from recipients
            try:
                to = [UserModel.objects.get(username = form.cleaned_data['to']).email]
            except:
                to = [form.cleaned_data['to']]
        if controller.email_options == '1':
            to = [r.email for r in controller.recipients.all()]
            for r in controller.other_recipients.all():
                to.append(r.email)

        if controller.send_emails:
            mail = EmailMessage(
                subject = subject,
                body = body,
                from_email = form.cleaned_data['sender_email'],
                to = to
            )
            if 'photo' in request.FILES:
                photo = request.FILES['photo']
                mail.attach(photo.name, photo.read(), photo.content_type)
            mail.send()
        if 'send_a_copy' in form.cleaned_data:
            mail = EmailMessage(
                subject = subject,
                body = body,
                from_email = form.cleaned_data['sender_email'],
                to = form.cleaned_data['sender_email']
            )
            mail.send()
        return render(request, 'success_url', {'controller': controller})

    return render(request, 'contact/form.html', {
        'form': form,
        'site': site,
        'controller': controller
    })
