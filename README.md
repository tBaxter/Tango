Tango
=====

Faster, simpler django content management.


##Installation:

Install via pip:
    pip install git+https://github.com/tBaxter/Tango.git

Add the apps you want to installed_apps:
    INSTALLED_APPS = (
        ...
        'articles',
        'galleries',
        'contact_manager'
    )

Run syncdb or South.

##Dependencies:
Python-Twitter: https://github.com/bear/python-twitter (if you want to auto-tweet news items)
Easy-Thumbnails: https://github.com/SmileyChris/easy-thumbnails
