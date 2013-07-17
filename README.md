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