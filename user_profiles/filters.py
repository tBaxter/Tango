import django_filters

from django.contrib.auth import get_user_model

UserModel = get_user_model()


class ProfileFilter(django_filters.FilterSet):
    display_name = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        model = UserModel
        fields = ['display_name']
