from django.urls import include, path

urlpatterns = [
    path('profiles/', include('tango_user.urls')),
    path('video/', include('video.urls')),
]
