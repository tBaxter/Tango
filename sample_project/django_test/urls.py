from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    # url(r'^django_test/', include('django_test.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^articles/', include('articles.urls.article_urls')),
    url(r'^contact/', include('contact_manager.urls')),
    url(r'^photos/', include('galleries.urls')),
    url(r'^events/', include('happenings.urls')),
    url(r'^profiles/', include('happenings.urls')),
    url(r'^video/', include('happenings.urls')),
)
