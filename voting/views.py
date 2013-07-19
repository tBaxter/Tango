from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import loader, RequestContext
from django.utils import simplejson

from models import Vote

VOTE_DIRECTIONS = (('up', 1), ('down', -1), ('clear', 0))


@login_required
def generic_vote_on_object(request, model_name, object_id, direction,
    post_vote_redirect=None, template_name=None,
        template_loader=loader, extra_context=None, context_processors=None,
        template_object_name='object', allow_xmlhttprequest=False):
    """
    Really generic object vote function.
    Gets object and model via content_type.
    Expects URL format:
    {% url 'generic_vote' 'content_type' object.id '<direction>' %}

    The given template will be used to confirm the vote if this view is
    fetched using GET; vote registration will only be performed if this
    view is POSTed.

    If ``allow_xmlhttprequest`` is ``True`` and an XMLHttpRequest is
    detected by examining the ``HTTP_X_REQUESTED_WITH`` header, the
    ``xmlhttp_vote_on_object`` view will be used to process the
    request - this makes it trivial to implement voting via
    XMLHttpRequest with a fallback for users who don't have JavaScript
    enabled.

    Templates:``<app_label>/<model_name>_confirm_vote.html``
    Context:
        object
            The object being voted on.
        direction
            The type of vote which will be registered for the object.
    """

    try:
        vote = dict(VOTE_DIRECTIONS)[direction]
    except KeyError:
        raise AttributeError('\'%s\' is not a valid vote type.' % direction)

    # TO-DO: check by app_label, also
    ctype = ContentType.objects.filter(model=model_name)[0]
    obj   = ctype.get_object_for_this_type(pk=object_id)

    if request.is_ajax() and request.method == 'GET':
        return json_error_response('XMLHttpRequest votes can only be made using POST.')

    Vote.objects.record_vote(obj, request.user, vote)

    if request.is_ajax():
        return HttpResponse(simplejson.dumps({'success': True,
                                          'score': Vote.objects.get_score(obj)}))

    if extra_context is None:
        extra_context = {}

    # Look up the object to be voted on
    if request.method == 'POST':
        if post_vote_redirect is not None:
            next = post_vote_redirect
        elif 'next' in request.REQUEST:
            next = request.REQUEST['next']
        elif hasattr(obj, 'get_absolute_url'):
            if callable(getattr(obj, 'get_absolute_url')):
                next = obj.get_absolute_url()
            else:
                next = obj.get_absolute_url
        else:
            raise AttributeError('Generic vote view must be called with either post_vote_redirect, a "next" parameter in the request, or the object being voted on must define a get_absolute_url method or property.')
        Vote.objects.record_vote(obj, request.user, vote)
        return HttpResponseRedirect(next)
    else:
        if not template_name:
            template_name = 'voting/confirm_vote.html'
        t = template_loader.get_template(template_name)
        c = RequestContext(request, {
            template_object_name: obj,
            'direction': direction,
        }, context_processors)
        for key, value in extra_context.items():
            if callable(value):
                c[key] = value()
            else:
                c[key] = value
        response = HttpResponse(t.render(c))
        return response


def json_error_response(error_message, *args, **kwargs):
    return HttpResponse(simplejson.dumps(dict(success=False,
                                              error_message=error_message)))
