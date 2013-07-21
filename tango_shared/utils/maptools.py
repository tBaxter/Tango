import urllib
import xmltramp

from django.conf import settings


def get_geocode(city, state, street_address="", zipcode=""):
    """
    For given location or object, takes address data and returns
    latitude and longitude coordinates from Google geocoding service

    get_geocode(self, street_address="1709 Grand Ave.", state="MO", zip="64112")

    Returns a tuple of (lat, long)
    Most times you'll want to join the return.

    """
    try:
        key = settings.GMAP_KEY
    except:
        return "You need to put GMAP_KEY in settings"

    # build valid location string
    location = ""
    if street_address:
        safeaddr = street_address.replace(" ", "+")
        location += '%s+' % safeaddr
    safecity = city.replace(" ", "+")
    location += '%s+%s' % (safecity, state)
    if zipcode:
        location += "+%s" % zipcode

    url = "http://maps.google.com/maps/geo?q=%s&output=xml&key=%s" % (location, key)
    file = urllib.urlopen(url).read()
    try:
        xml = xmltramp.parse(file)
    except:
        print "Failed to parse xml:" + file
        return None

    status = str(xml.Response.Status.code)
    if status == "200":
        geocode = str(xml.Response.Placemark.Point.coordinates).split(',')
         # Flip geocode because geocoder returns long/lat. Maps wants lat/long.
        return (geocode[1], geocode[0])
    else:
        print status
        return None
