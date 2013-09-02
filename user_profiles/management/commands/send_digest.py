import datetime
import time

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template import Context
from django.template.loader import get_template


UserModel = get_user_model()
today = datetime.date.today()
one_day_ago = today - datetime.timedelta(days=1)
last_seen_timestamp = time.mktime(one_day_ago.timetuple())


class Command(BaseCommand):
    help = 'Sends email digest of new activity to users who requested one.'

    def handle(self, *args, **options):
        count = 0
        site = Site.objects.get_current()
        for user in UserModel.objects.filter(get_digest=1):
            subject = '{} Digest for {}'.format(site.name, today.strftime("%A, %B %e"))

            watchlist = []
            watch_objects = [w.content_object for w in user.watch_set.all()]
            for obj in watch_objects:
                if hasattr(obj, 'modified') and (obj.modified.date() > one_day_ago or obj.modified_int > last_seen_timestamp):
                    watchlist.append(obj)

            c = Context({
                'user': user,
                'subject': subject,
                'last_seen': one_day_ago,
                'today': today,
                'watchlist': watchlist,
                'site': site,
                'site_root': 'http://{}'.format(site.domain),
                'theme': user.theme
            })
            tmpl = get_template('users/digest.html')

            body = tmpl.render(c)
            msg = EmailMultiAlternatives(
                subject,
                body,
                settings.ADMINS[0]
                [user.email]
            )
            msg.attach_alternative(body, "text/html")
            msg.send()
            count += 1
