import datetime

from django import template
from django.utils.timesince import timesince

register = template.Library()


@register.inclusion_tag('includes/formatted_time.html')
def format_time(date_obj, time_obj=None, datebox=False, dt_type=None):
    """
    Returns formatted HTML5 elements based on given datetime object.
    By default returns a time element, but will return a .datebox if requested.

    dt_type allows passing dt_start or dt_end for hcal formatting.
    link allows passing a url to the datebox.

    Usage:
    {% format_time obj.pub_date %}
    {% format_time obj.start_date 'datebox' 'dtstart' %}
    {% format_time obj.end_date obj.end_time 'datebox' 'dt_end' %}
    """
    if not time_obj:
        try:
            time_obj = date_obj.time
        except:
            time_obj = None
    return {
        'date_obj': date_obj,
        'time_obj': time_obj,
        'datebox': datebox,
        'current_year': datetime.date.today().year,
        'dt_type': dt_type,
    }


@register.filter
def short_timesince(date):
    """
    A shorter version of Django's built-in timesince filter.
    Selects only the first part of the returned string,
    splitting on the comma.

    Falls back on default Django timesince if it fails.

    Example: 3 days, 20 hours becomes "3 days".

    """
    try:
        return timesince(date).split(", ")[0]
    except IndexError():
        timesince(date)


@register.filter
def fix_indents(value):
    """
    Strips tabs and extra spaces from user-submitted text
    to avoid triggering pre code in markdown.

    Use this with caution.
    It's much better to sanitize the content before save().

    Likely to be replaced by a smarter minification.
    """
    value = value.replace('\t', '').replace('    ', ' ')
    return value
