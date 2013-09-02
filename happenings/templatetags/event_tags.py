import datetime

from django import template
from django.contrib.sites.models import Site
from happenings.models import Event, GiveawayResponse, Update

register = template.Library()

today = datetime.date.today()
current_site = Site.objects.get_current()


@register.assignment_tag
def get_upcoming_events_count(days=14, featured=False):
    """
    Returns count of upcoming events for a given number of days, either featured or all
    Usage:
    {% get_upcoming_events_count DAYS as events_count %}
    with days being the number of days you want, or 5 by default
    """
    start_period  = today - datetime.timedelta(days=2)
    end_period    = today + datetime.timedelta(days=days)
    if featured:
        return Event.objects.filter(featured=True, start_date__gte=start_period, start_date__lte=end_period).count()
    return Event.objects.filter(start_date__gte=start_period, start_date__lte=end_period).count()


@register.assignment_tag
def get_upcoming_events(num, days, featured=False):
    """
    Get upcoming events.
    Allows slicing to a given number,
    picking the number of days to hold them after they've started
    and whether they should be featured or not.
    Usage:
    {% get_upcoming_events 5 14 featured as events %}
    Would return no more than 5 Featured events,
    holding them for 14 days past their start date.

    """
    offset = today - datetime.timedelta(days=days)
    events = Event.objects.filter(start_date__gt=offset).order_by('start_date')
    if featured:
        events = events.filter(featured=True)
    events = events[:num]
    return events


@register.assignment_tag
def get_events_by_date_range(days_out, days_hold, max_num=5, featured=False):
    """
    Get upcoming events for a given number of days (days out)
    Allows specifying number of days to hold events after they've started
    The max number to show (defaults to 5)
    and whether they should be featured or not.
    Usage:
    {% get_events_by_date_range 14 3 3 'featured' as events %}
    Would return no more than 3 featured events,
    that fall within the next 14 days or have ended within the past 3.
    """
    range_start = today - datetime.timedelta(days=days_hold)
    range_end   = today + datetime.timedelta(days=days_out)

    events = Event.objects.filter(start_date__gte=range_start, start_date__lte=range_end).order_by('start_date')
    if featured:
        events = events.filter(featured=True)
    events = events[:max_num]
    return events


@register.inclusion_tag('happenings/includes/event_subnav.html')
def load_event_subnav(event, user=None, use_domain=False):
    context = {
        'event': event,
        'user': user,
    }
    if use_domain:
        context['domain'] = 'http://{}'.format(current_site.domain)
    return context


@register.inclusion_tag('happenings/includes/past_events.html')
def load_past_events():
    today = datetime.date.today() - datetime.timedelta(days=2)
    return {'events': Event.objects.filter(start_date__lt=today, featured=True)}


@register.inclusion_tag('happenings/giveaways/winners.html')
def render_giveaway_winners(giveaway):
    """
    shows giveaway winners
    """
    return {
        'winners': GiveawayResponse.objects.filter(question=giveaway, correct=True),
        'giveaway': giveaway
    }


@register.inclusion_tag('includes/pagination/prev_next.html')
def paginate_update(update):
    """
    attempts to get next and previous on updates
    """
    time  = update.pub_time
    event = update.event
    try:
        next = Update.objects.filter(event=event, pub_time__gt=time).order_by('pub_time').only('title')[0]
    except:
        next = None
    try:
        previous = Update.objects.filter(event=event, pub_time__lt=time).order_by('-pub_time').only('title')[0]
    except:
        previous = None
    return {'next': next, 'previous': previous, 'event': event}
