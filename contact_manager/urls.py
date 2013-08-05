from django.conf.urls import patterns, url


urlpatterns = patterns(
    'contact_manager.views',
    url(
        regex=r'^$',
        name="site_contact_form",
        view='simple_contact'
    ),
    url(
        regex=r'^members/(?P<username>[-\w]+)/$',
        name="member_contact_form",
        view='simple_contact'
    ),
    url(
        regex=r'^done/$',
        name="contact_done",
        view='contact_done',
    ),
    url(
        regex=r'^messages/$',
        name="contact_list",
        view='contact_list'
    ),
    url(
        regex=r'^messages/(?P<pk>[\d]+)/$',
        name='contact_detail',
        view='contact_detail',
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/$',
        name="contact_form_builder",
        view='build_contact'
    ),
    url(
        regex=r'^(?P<controller_slug>[-\w]+)/messages/$',
        name="controller_contact_list",
        view='form_contact_list'
    ),
)
