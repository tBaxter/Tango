from django.urls import path

from .views import video_list, video_gallery_list, video_detail, video_gallery_detail

urlpatterns = [
    path('', video_list, name="video_list"),
    path('galleries/', video_gallery_list, name="video_gallery_list"),
    path('<slug:slug>/', video_detail, name='video_detail'),
    path('gallery/<slug:slug>/', video_gallery_detail, name='video_gallery_detail'),
]
