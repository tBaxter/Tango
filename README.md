Tango
=====

Faster, simpler django content management.


##Installation:

Install via pip:
    pip install git+https://github.com/tBaxter/Tango.git

Add the apps you want to installed_apps. You really should add tango_shared, as a lot relies on it.
    INSTALLED_APPS = (
        ...
        'articles',
        'galleries',
        'contact_manager',
        'tango_shared'
    )

Run syncdb or South.

##Dependencies:
[Easy-Thumbnails](https://github.com/SmileyChris/easy-thumbnails)
PIL or Pillow
Markdown
Typogrify
[Python-Twitter](https://github.com/bear/python-twitter) (if you want to auto-tweet news items)

### Recommended
South
docutils
