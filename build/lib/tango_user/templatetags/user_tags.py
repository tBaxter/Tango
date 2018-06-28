import datetime

from django import template
from django.contrib.auth import get_user_model

UserModel = get_user_model()

register = template.Library()

today = datetime.date.today()
one_day_ago = datetime.datetime.now() - datetime.timedelta(days=1)


@register.assignment_tag
def get_birthday_list():
    """
    Returns today's birthdays
    Usage:
    {% get_birthday_list as birthday_list %}
    """
    return UserModel.objects.filter(is_active=True, birthday__month = today.month, birthday__day = today.day).values()


@register.assignment_tag
def get_new_members(count=5):
    """
    Returns most recent new members.
    Usage:
    {% get_new_members NUM as new_members %}
    with NUM being the number you want, or 5 by default

    or you can pass 'today' in, and get new members for today:
    {% get_new_members 'today' as new_members %}

    """
    if count != 'today':
        return UserModel.objects.filter(is_active=True).order_by('-id')[:count]
    return UserModel.objects.filter(is_active=True, date_joined__gte=one_day_ago).order_by('-id')
