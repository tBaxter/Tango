from django.conf.urls import *
from django.views.generic import DetailView

from articles.views import ArticleDetail, ArticleList

urlpatterns = patterns(
    '',
    url(
        regex=r'^(?P<slug>[-\w]+)/$',
        view=ArticleDetail.as_view(),
        name="article_detail"
    ),
    url(
        regex=r'^$',
        view=ArticleList.as_view(),
        name="article_list"
    ),
    url(
        regex=r'^briefs/(?P<id>[-\d]+)/$',
        view=DetailView.as_view(),
        name="brief_detail"
    ),
)
