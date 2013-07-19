from .models import Article

import django_filters


class ArticleFilter(django_filters.FilterSet):
    headline = django_filters.CharFilter(lookup_type='icontains')
    body     = django_filters.CharFilter(label="Description", lookup_type='icontains')

    class Meta:
        model = Article
        fields = ['headline', 'body']
