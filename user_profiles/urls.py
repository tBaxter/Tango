from django.conf.urls import *
from django.views.generic import TemplateView

from contact.views import contact
from songs.views import delete_songs
from user_profiles.views import *


urlpatterns = patterns('',
    url(
        r'^$',
        MemberList.as_view(),
        name="community_index"
    ),
    #url(r'^edit/(?P<slug>[-\w]+)/$', EditProfile.as_view(), name="edit_profile"),
    #url(r'^edit/(?P<pk>\d+)/$',      login_required(EditProfile.as_view()), name="edit_profile"),
    #url(r'^edit/$', 		         EditProfile.as_view(), name="edit_profile_simple"),
    url(
        r'^edit-profile/$',
        EditProfile.as_view(),
        name="edit_profile"
    ),
        url(
        r'^edit-settings/$',
        EditProfileSettings.as_view(),
        name="edit_settings"
    ),
    url(
        regex=r'^(?P<pk>\d+)/$',
        view=view_profile,
        name="view_profile_by_id"
    ),
    url(
        r'^(?P<slug>[-\w]+)/$',
        view_profile,
        name='view_profile'
    ),
    url(
        regex=r'^contact/(?P<slug>[-\w]+)/$',
        view=contact,
        name="contact_member"
    ),
    (r'^contact/(?P<slug>[-\w]+)/done/$', TemplateView.as_view(template_name='contact/done.html')),
    (r'^(?P<slug>[-\w]+)/delete-songs/$', delete_songs),
)
