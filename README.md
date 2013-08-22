Tango
=====

Faster, simpler django content management.


##Installation:

###Install via pip:

    pip install django-tango

Or, if you want the very latest version from GitHub:

    pip install git+https://github.com/tBaxter/Tango.git

If you're installing in a fresh, brand-new virtualenvironment -- and you are using a virtualenvironment, right? -- then you'll see a lot of stuff fly by. 
Don't worry, that's just the dependencies. 
If your environment already has the usual stuff installed (Django, PIL, etc), 
then you'll speed through the Tango install. 

For more info, see the "Dependencies" section.

###For a new project, run the [Tango Starter Kit](https://github.com/tBaxter/tango-starter-kit): 

    django-admin.py startproject --template=https://github.com/tBaxter/tango-starter-kit/archive/master.zip test_project

*Note: test_project should (of course) be changed to the name of your project*

### What then?
If you used the starter project, a basic test database was included. 
Just run manage.py runserver and you'll have a working site. 
You can log into the admin with username:admin, password:test.
Obviously, you'll want to change that right away.

If not, you'll want to run syncdb or South.

Then start adding content. That's it.

### Before you go live
Before the site is ready to go live, you'll want to change some settings and hook up a real database, of course.
Before users can register and sign in, you'll also need to configure user registration and authentication. We like [django-allauth](https://github.com/pennersr/django-allauth), but have also used and liked django-registration.


##Dependencies (these should be installed for you)
[Django 1.5.1 +](https://www.djangoproject.com)  
PIL or Pillow (Your choice)  
[Easy-Thumbnails](https://github.com/SmileyChris/easy-thumbnails)    
Markdown & Typogrify for nice text formatting   
django-filter  
vobject
[Python-Twitter](https://github.com/bear/python-twitter) (if you want to auto-tweet news items)

### Recommended
South  
docutils  
