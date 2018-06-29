from django.urls import path

from .views import member_index, edit_profile, edit_settings, view_profile

urlpatterns = [
    path('', member_index, name="community_index"),
    path('edit-profile/', edit_profile, name="edit_profile"),
    path('edit-settings/', edit_settings, name="edit_settings"),
    path('<int:pk>/', view_profile, name="view_profile_by_id"),
    path('<slug:slug>/', view_profile, name='view_profile'),
]
