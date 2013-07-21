from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    url(r'^articles/', include('articles.urls.article_urls')),
    url(r'^contact/', include('contact_manager.urls')),
    url(r'^photos/', include('galleries.urls')),
    url(r'^events/', include('happenings.urls')),
    url(r'^profiles/', include('happenings.urls')),
    url(r'^video/', include('happenings.urls')),
)
