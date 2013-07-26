from django.conf import settings
from django.views.generic import ListView, DetailView

from .models import Video, VideoGallery

paginate_by = getattr(settings, "PAGINATE_BY", 25)


class VideoList(ListView):
    """
    Returns a list of all videos.
    """
    template_name = 'video/video_list.html'
    paginate_by = paginate_by
    model = Video
video_list = VideoList.as_view()


class VideoDetail(DetailView):
    """
    Returns a video detail
    """
    template_name = 'video/video_detail.html'
    model = Video
video_detail = VideoDetail.as_view()


class VideoGalleryList(ListView):
    """
    Returns a list of all video Galleries.
    """
    template_name = 'video/gallery_list.html'
    paginate_by = paginate_by
    model = VideoGallery
video_gallery_list = VideoGalleryList.as_view()


class VideoGalleryDetail(DetailView):
    """
    Returns a gallery detail
    """
    template_name = 'video/video_list.html'
    model = VideoGallery
    context_object_name = 'gallery'

    def get_context_data(self, **kwargs):
        context = super(VideoGalleryDetail, self).get_context_data(**kwargs)
        context.update({
            'object_list' : self.get_object().video_collection.all(),
        })
        return context
video_gallery_detail = VideoGalleryDetail.as_view()
