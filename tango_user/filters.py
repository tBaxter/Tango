import django_filters

from django.contrib.auth import get_user_model



class ProfileFilter(django_filters.FilterSet):
    display_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = get_user_model()
        fields = ['display_name']
