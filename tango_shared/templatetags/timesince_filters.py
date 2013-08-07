from django import template
from django.utils.timesince import timesince
register = template.Library()


@register.filter
def short_timesince(date):
	"""
	selects only the first part of the returned string, splitting on the comma from timesince.
	Ex. 3 days, 20 hours becomes "3 days ago"
	"""
	try:
		ago = timesince(date).split(",")[0]
	except: # can't get valid datetime !?!
		ago = "some time"
	return ago