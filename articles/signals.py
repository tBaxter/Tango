import twitter

from django.conf import settings

TWITTER_MAXLENGTH = getattr(settings, 'TWITTER_MAXLENGTH', 140)


def auto_tweet(sender, instance, *args, **kwargs):
    """
    Allows auto-tweeting newly created object to twitter
    on accounts configured in settings.

    You MUST create an app to allow oAuth authentication to work:
     -- https://dev.twitter.com/apps/
    You also must set the app to "Read and Write" access level,
    and create an access token. Whew.
    """

    if not kwargs.get('created'):
        return False

    try:
        twitter_key = settings.TWITTER_SETTINGS
    except AttributeError:
        print 'WARNING: Twitter account not configured.'
        return False

    try:
        api = twitter.Api(
            consumer_key        = twitter_key['consumer_key'],
            consumer_secret     = twitter_key['consumer_secret'],
            access_token_key    = twitter_key['access_token_key'],
            access_token_secret = twitter_key['access_token_secret']
        )
    except Exception, inst:
        print "failed to authenticate: %s" % (inst)

    #print 'authenticated with twitter'
    text = instance.text

    if instance.link:
        link = instance.link
    else:
        link = instance.get_absolute_url()

    text = '%s %s' % (text, link)

    try:
        api.PostUpdate(text)
    except Exception, inst:
        print "Error posting to twitter: %s" % inst
