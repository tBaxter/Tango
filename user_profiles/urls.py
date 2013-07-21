from django.conf.urls import patterns, url

urlpatterns = patterns(
    'user_profiles.views',
    url(
        regex=r'^$',
        view='member_index',
        name="community_index"
    ),
    url(
        regex=r'^edit-profile/$',
        view='edit_profile',
        name="edit_profile"
    ),
    url(
        regex=r'^edit-settings/$',
        view='edit_settings',
        name="edit_settings"
    ),
    url(
        regex=r'^(?P<pk>\d+)/$',
        view='view_profile',
        name="view_profile_by_id"
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/$',
        view='view_profile',
        name='view_profile'
    ),
)
