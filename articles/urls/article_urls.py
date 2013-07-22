from django.conf.urls import patterns, url
from django.views.generic import DetailView


urlpatterns = patterns(
    'articles.views',
    url(
        regex=r'^(?P<slug>[-\w]+)/$',
        view='article_detail',
        name="article_detail"
    ),
    url(
        regex=r'^$',
        view='article_list',
        name="article_list"
    ),
)

urlpatterns += patterns(
    '',
    url(
        regex=r'^briefs/(?P<id>[-\d]+)/$',
        view=DetailView.as_view(),
        name="brief_detail"
    ),
)
