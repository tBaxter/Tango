from django.conf import settings
from django.conf.urls import *
from django.views.generic import DetailView, TemplateView

from .models import *
from .views import *

key = getattr(settings, 'GMAP_KEY', None)

urlpatterns = patterns(
    'happenings.views',
    # CRUD and admin functions
    url(
        regex=r'^add/$',
        view='add_event',
        name="add_event"
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/edit-event/$',
        view=EditEvent.as_view(),
        name="edit-event"
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/add-recap/$',
        view=AddRecap.as_view(),
        name="add_recap"
    ),

    # EVENT LISTS
    url(
        regex=r'^$',
        view=EventList.as_view(),
        name="events_index"
    ),
    url(
        regex=r'^by-region/(?P<region>[-\w]+)/$',
        view=EventList.as_view(),
        name="events_by_region"
    ),
    url(
        regex=r'^by-state/(?P<state>[-\w]+)/$',
        view=EventList.as_view(),
        name="events_by_state"),
    url(
        regex=r'^(?P<m>\d{2})/(?P<d>\d{2})/(?P<y>\d{4})/$',
        view=EventsForPeriod.as_view(),
        name="events_for_day"
    ),
    url(
        name="events_for_month",
        regex=r'^(?P<m>\d{2})/(?P<y>\d{4})/$',
        view=EventsForPeriod.as_view(),
    ),


    # ************* EVENT DETAILS *************/
    url(
        name="event_detail",
        regex=r'^(?P<slug>[-\w]+)/$',
        view=EventDetail.as_view(),
    ),

    # add to calendar
    url(
        name="event_ical",
        regex=r'^(?P<slug>[-\w]+)/ical/$',
        view='create_ical',
    ),

    # **************** Event children ************/
    # slideshow
    url(
        name="event_slides",
        regex=r'^(?P<slug>[-\w]+)/slides/$',
        view=EventDetail.as_view(template_name="happenings/event_slides.html"),
    ),
    # videos
    url(
        name="event_video_list",
        regex=r'^(?P<slug>[-\w]+)/videos/$',
        view='video_list',
    ),
    # map
    url(
        name="event_map",
        regex=r'^(?P<slug>[-\w]+)/map/$',
        view=EventDetail.as_view(template_name="happenings/event_map.html"),
    ),

    url(
        name="event_comments",
        regex=r'^(?P<slug>(\w|-)+)/all-comments/$',
        view='event_all_comments_list',
    ),

    # attending
    url(
        name='event_attending_list',
        regex=r'^(?P<slug>[-\w]+)/attending/$',
        view=EventDetail.as_view(template_name="happenings/attending/list.html"),
    ),
    url(
        name="attending_add",
        regex=r'^(?P<slug>[-\w]+)/attending/add/$',
        view='add_attending',
    ),

    # memories
    url(
        name="add_memory",
        regex=r'^(?P<slug>[-\w]+)/memories/add/$',
        view='add_memory',
    ),
    url(
        name="event_memories",
        regex=r'^(?P<slug>(\w|-)+)/memories/$',
        view=DetailView.as_view(
            queryset=Event.objects.all(),
            template_name="happenings/memory_list.html",
        ),
    ),
    url(
        name="memory_detail",
        regex=r'^(?P<event_slug>(\w|-)+)/memories/(?P<pk>\d+)/',
        view=MemoryDetail.as_view(),
    ),

    # extra info pages
    url(
        name="special_event_extra",
        regex=r'^(?P<event_slug>(\w|-)+)/extra/(?P<slug>(\w|-)+)/',
        view=ExtraInfoDetail.as_view(),
    ),

    # update list
    url(
        name="event_update_list",
        regex=r'^(?P<slug>[-\w]+)/updates/$',
        view='event_update_list',
    ),

    # update detail
    url(
        name="event_update_detail",
        regex=r'^(?P<event_slug>(\w|-)+)/updates/(?P<pk>\d+)/',
        view=EventUpdate.as_view(),
    ),

    # GIVEAWAYS
    url(
        name="giveaways",
        regex=r'^(?P<slug>[-\w]+)/giveaways/$',
        view='giveaways_for_event',
    ),
    url(
        name="giveaway_winner",
        regex=r'^(?P<slug>[-\w]+)/giveaways/winners/$',
        view='giveaway_winners_for_event',
    ),
    url(
        name="giveaway_response_processing",
        regex=r'^giveaways/(?P<giveaway_id>\d+)/response/$',
        view='record_giveaway_response',
    ),
    url(
        name="giveaway_response_recorded",
        regex=r'^giveaway/response-recorded/$',
        view=TemplateView.as_view(template_name="happenings/response_recorded.html"),
    ),

    # PLAYLIST
    url(
        name="playlist",
        regex=r'^(?P<slug>[-\w]+)/playlist/$',
        view='playlist',
    ),
)
