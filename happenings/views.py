import calendar
import datetime
import vobject

from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.defaultfilters import slugify
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, UpdateView

from .forms import GiveawayResponseForm, PlayListForm, MemoryForm, AddEventForm, EventRecapForm, EventUpdateForm
from .models import Event, Update, Giveaway, GiveawayResponse, PlaylistItem, Image, ExtraInfo, Memory

key = getattr(settings, 'GMAP_KEY', None)


class EventList(ListView):
    """
    Returns a paginated list of events.
    """
    region = state = None
    template_name = 'happenings/index.html'
    paginate_by   = 100

    def get_queryset(self):
        now = datetime.date.today()
        offset = now - datetime.timedelta(days=5)
        events = Event.objects.filter(approved=True, start_date__gte=offset).order_by('start_date')
        if 'region' in self.kwargs:
            self.region = self.kwargs['region']
            events = events.filter(region=self.kwargs['region'])
        return events

    def get_context_data(self, **kwargs):
        context = super(EventList, self).get_context_data(**kwargs)
        context['region'] = self.region
        return context
event_list = EventList.as_view()


class EventsForPeriod(EventList):
    month = day = year = None

    def get_queryset(self, *args, **kwargs):
        qs = super(EventsForPeriod, self).get_queryset(*args, **kwargs)
        self.month = int(self.kwargs['m'])
        self.year = int(self.kwargs['y'])
        if 'd' in self.kwargs:
            self.day  = int(self.kwargs['d'])
            start_date = end_date = datetime.date(self.year, self.month, self.day)
            qs = qs.filter(start_date__lte=start_date, end_date__gte=end_date)
        else:
            start_date = datetime.date(self.year, self.month, 1)
            end_date   = datetime.date(self.year, self.month, calendar.monthrange(self.year, self.month)[1])
            qs = qs.filter(start_date__gte=start_date, end_date__lte=end_date)
        return qs

    def get_context_data(self, **kwargs):
        context = super(EventsForPeriod, self).get_context_data(**kwargs)
        if self.day:
            date = datetime.date(self.year, self.month, self.day)
            cal_type = 'day'
        else:
            date = datetime.date.strftime(datetime.date(self.year, self.month, 1), '%B %Y')
            cal_type = 'month'
        context.update({
            'cal_date' : date,
            'cal_type' : cal_type
        })
        return context
events_for_period = EventsForPeriod.as_view()


class EventDetail(DetailView):
    queryset = Event.objects.all()

    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        context['key'] = key
        return context
event_detail = EventDetail.as_view()


class EventUpdate(DetailView):
    """
    Detail page for an Event.Update.
    """
    template_name = "happenings/updates/update_detail.html"

    def dispatch(self, request, *args, **kwargs):
        self.event_slug = kwargs.get('event_slug', False)
        self.slug = kwargs.get('slug', False)
        self.event = get_object_or_404(Event, slug=self.event_slug)
        return super(EventUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EventUpdate, self).get_context_data(**kwargs)
        context['event'] = self.event
        return context

    def get_object(self):
        return get_object_or_404(Update, pk=self.kwargs.get('pk', None))


class ExtraInfoDetail(EventUpdate):
    """
    Detail page for an Event.ExtraInfo, if it's not a sidebar.
    """
    queryset = ExtraInfo.objects.filter(is_sidebar=False)
    template_name = "happenings/event_extra.html"

    def get_object(self):
        return get_object_or_404(ExtraInfo, slug=self.slug)


def create_ical(request, slug):
    """ Creates an ical .ics file for an event using vobject. """
    event    = get_object_or_404(Event, slug=slug)
    # convert dates to datetimes.
    # when we change code to datetimes, we won't have to do this.
    start = event.start_date
    start = datetime.datetime(start.year, start.month, start.day)

    if event.end_date:
        end = event.end_date
        end = datetime.datetime(end.year, end.month, end.day)
    else:
        end = start

    cal = vobject.iCalendar()
    cal.add('method').value = 'PUBLISH'
    vevent = cal.add('vevent')
    vevent.add('dtstart').value = start
    vevent.add('dtend').value = end
    vevent.add('dtstamp').value = datetime.datetime.now()
    vevent.add('summary').value = event.name
    response = HttpResponse(cal.serialize(), mimetype='text/calendar')
    response['Filename'] = 'filename.ics'
    response['Content-Disposition'] = 'attachment; filename=filename.ics'
    return response


def event_all_comments_list(request, slug):
    """
    Returns a list view of all comments for a given event.
    Combines event comments and update comments in one list.
    """
    event    = get_object_or_404(Event, slug=slug)
    comments = event.get_all_comments()
    page = int(request.GET.get('page', 1))
    is_paginated = False
    if comments:
        paginator = Paginator(comments, 50)  # Show 50 comments per page
        try:
            comments = paginator.page(page)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            comments = paginator.page(paginator.num_pages)
        is_paginated = comments.has_other_pages()

    return render(request, 'happenings/event_comments.html', {
        "event": event,
        "comment_list": comments,
        "page_obj": page,
        "is_paginated": is_paginated,
        "key": key
    })


def event_update_list(request, slug):
    """
    Returns a list view of updates for a given event.
    If the event is over, it will be in chronological order.
    If the event is upcoming or still going,
    it will be in reverse chronological order.
    """
    event = get_object_or_404(Event, slug=slug)
    updates = Update.objects.filter(event__slug=slug)
    has_started = True
    if event.ended():  # if the event is over, use chronological order
        updates.order_by('id')
    else:  # if not, use reverse chronological
        updates.order_by('-id')
    return render(request, 'happenings/updates/update_list.html', {
      'event': event,
      'object_list': updates,
      'has_started': has_started,
    })


def video_list(request, slug):
    """
    Displays list of videos for given event.
    """
    event = get_object_or_404(Event, slug=slug)
    return render(request, 'video/video_list.html', {
        'event': event,
        'video_list': event.eventvideo_set.all()
    })


def giveaways_for_event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    giveaways = Giveaway.objects.filter(event__slug=slug)
    return render(request, 'happenings/giveaways/giveaway_list.html', {
        'event': event,
        'giveaways': giveaways,
    })


def giveaway_winners_for_event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    winners = GiveawayResponse.objects.filter(question__event__slug=slug, correct=True).order_by('respondent__id')

    template_name = 'happenings/giveaways/winners.html'
    if 'export' in request.GET:
        template_name = 'happenings/giveaways/winners_export.html'

    return render(request, template_name, {
        'event': event,
        'winners': winners,
    })


def playlist(request, slug):
    event    = get_object_or_404(Event, slug=slug)
    playlist = PlaylistItem.objects.filter(event=event).order_by('-votes')
    form = PlayListForm()
    if request.method == 'POST':
        data = request.POST.copy()
        data['user'] = request.user.id
        data['event'] = event.id
        form = PlayListForm(data, request.FILES)
        if form.is_valid():
            form.save()
    return render(request, 'happenings/playlist.html', {
        'form': form,
        'playlist_items': playlist,
        'event': event
    })


@login_required
def add_event(request):
    """ Public form to add an event. """
    form = AddEventForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.sites = settings.SITE_ID
        instance.submitted_by = request.user
        instance.approved = True
        instance.slug = slugify(instance.name)
        instance.save()
        messages.success(request, 'Your event has been added.')
        return HttpResponseRedirect(reverse('events_index'))
    return render(request, 'happenings/event_form.html', {'form': form, 'form_title': 'Add an event'})


class EditEvent(UpdateView):
    model = Event
    form_class = EventUpdateForm
    template_name = "happenings/event_form.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if user.is_staff is False and user != self.get_object().submitted_by:
            raise forms.ValidationError("You don't have permission to edit this event.")
        return super(EditEvent, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EditEvent, self).get_context_data(**kwargs)
        context['form_title'] = "Edit your event"
        return context
edit_event = EditEvent.as_view()


class AddRecap(EditEvent):
    form_class = EventRecapForm
add_recap = AddRecap.as_view()


@login_required
def add_attending(request, slug):
    event = get_object_or_404(Event, slug=slug)
    event.attending.add(request.user.id)
    event.save()
    if request.is_ajax():
        return HttpResponse(request.user.display_name, mimetype="text/html")
    return HttpResponseRedirect(reverse('event_attending_list', args=[event.slug]))


def record_giveaway_response(request, giveaway_id):
    giveaway = get_object_or_404(Giveaway, id=giveaway_id)
    form = GiveawayResponseForm(request.POST or None)
    if form.is_valid():
        new_instance = form.save()
        new_instance.giveaway = giveaway
        new_instance.respondent = request.user
        new_instance.save()
        messages.sucess(request, 'Your response has been recorded.')
    try:
        return HttpResponseRedirect(giveaway.update_set.all()[0].get_absolute_url())
    except:
        return HttpResponseRedirect(reverse('events_index'))


def add_memory(request, slug):
    """ Adds a memory to an event. """
    event = get_object_or_404(Event, slug=slug)
    form = MemoryForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.event = event
        instance.save()
        msg = "Your thoughts were added. "
        if request.FILES:
            photo_list = request.FILES.getlist('upload')
            photo_count = len(photo_list)
            for upload_file in photo_list:
                process_upload(upload_file, instance, form, event, request)
            if photo_count > 1:
                msg += "{} images were added and should appear soon.".format(photo_count)
            else:
                msg += "{} image was added and should appear soon.".format(photo_count)
        messages.success(request, msg)
        return HttpResponseRedirect('../')
    return render(request, 'happenings/add_memories.html', {'form': form, 'event': event})


class MemoryDetail(DetailView):
    """
    Creates a detail page for an Event.Memory.
    """
    template_name = "happenings/memory_detail.html"
    queryset = Memory.objects.all()

    def dispatch(self, request, *args, **kwargs):
        self.event_slug = kwargs.get('event_slug', False)
        self.slug = kwargs.get('slug', False)
        self.event = get_object_or_404(Event, slug=self.event_slug)
        return super(MemoryDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MemoryDetail, self).get_context_data(**kwargs)
        context['event'] = self.event
        return context

    def get_object(self):
        return get_object_or_404(Memory, pk=self.kwargs.get('pk', None))


def process_upload(upload_file, instance, form, event, request):
    """
    Helper function that actually processes and saves the upload(s).
    Segregated out for readability.
    """
    caption = form.cleaned_data.get('caption')
    upload_name = upload_file.name.lower()
    if upload_name.endswith('.jpg') or upload_name.endswith('.jpeg'):
        try:
            upload = Image(
                event   = event,
                image   = upload_file,
                caption = caption,
            )
            upload.save()
            instance.photos.add(upload)
        except Exception as error:
            messages.error(request, 'Error saving image: {}.'.format(error))
