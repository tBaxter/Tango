from django.conf.urls import patterns, url
from django.views.generic import TemplateView, ListView

from articles.models import Destination
from articles.views import ArticleDetail, ArticleList, EditBlogEntry, CreateBlogEntry


urlpatterns = patterns(
    '',
    url(
        name='add_entry_thanks',
        regex=r'^entry/thank-you/$',
        view=TemplateView.as_view(template_name='blogs/thank-you.html')
    ),

    url(
        name="blog_add_entry",
        regex=r'^(?P<destination_slug>[-\w]+)/add-entry/$',
        view=CreateBlogEntry.as_view()
    ),
    url(
        name="blog_add_image",
        regex=r'^(?P<destination_slug>[-\w]+)/(?P<entry_slug>[-\w]+)/add-images/$',
        view='articles.views.add_image'
    ),
    url(
        name="blog_edit_entry",
        regex=r'^(?P<blog_slug>[-\w]+)/edit-entry/(?P<pk>\d+)/$',
        view=EditBlogEntry.as_view()
    ),
    url(
        name="blog_list",
        regex=r'^$',
        view=ListView.as_view(
            queryset=Destination.blogs.all(),
            template_name='blogs/blog_list.html'
        )
    ),
    url(
        name="blog_detail",
        regex=r'^(?P<destination_slug>[-\w]+)/$',
        view=ArticleList.as_view(),
    ),
    url(
        name="blog_entry_detail",
        regex=r'^(?P<destination_slug>[-\w]+)/(?P<slug>[-\w]+)/$',
        view=ArticleDetail.as_view(),
    ),
)
