from django import template
from articles.models import Article, Brief

register = template.Library()


@register.assignment_tag
def get_latest_articles(num, assignment_slug=None, brief=False, *args, **kwargs):
    """
    Takes a given number and assignment slug and returns a list.
    Note that you can pass no assignment slug and it will return all articles.
    Usage:
        {% get_latest_articles 5 some_blog as blog_entries %}
        {% get_latest_articles 10 as latest_content %}
        {% get_latest_articles 5 brief=True as news_briefs %}
    """
    if brief:
        return Brief.objects.all().order_by('-id')[0:num]

    if assignment_slug:
        return Article.published.filter(assignment__slug=assignment_slug)[0:num]
    return Article.published.all()[0:num]


@register.assignment_tag
def get_new_articles(last_seen, assignment_slug=None, brief=False, *args, **kwargs):
    """
    Takes a 'last_seen' timestamp and assignment slug and returns a list.
    Note that you can pass no assignment slug and it will return all articles.
    Pass brief=True to get news briefs
    Usage:
        {% get_new_articles <LAST_SEEN> some_blog as blog_entries %}
        {% get_new_articles <LAST_SEEN> as latest_content %}
        {% get_new_articles <LAST_SEEN> brief=True as news_briefs %}
    """
    if brief:
        return Brief.objects.filter(pub_date__gte=last_seen).order_by('-id')

    if assignment_slug:
        return Article.published.filter(assignment__slug=assignment_slug, created__gte=last_seen)
    return Article.published.filter(created__gte=last_seen)
