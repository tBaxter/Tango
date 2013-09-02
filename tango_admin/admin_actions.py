from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import BlacklistForm
from .models import Blacklist


def nuke_users(modeladmin, request, queryset):
    """
    Deactivates user, removes their comments, deletes their session,
    and leaves a record of what they did to get nuked.

    This action can be used from user or comment admin.

    If you would like to use it in other model admins,
    you'll need to add appropriate content type handling.
    """
    users       = None
    form        = BlacklistForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
    contenttype = ContentType.objects.get_for_model(queryset.model)
    # Because we want this action available from comments or user admin lists, sort out content type
    if str(contenttype) == 'user':
        users = queryset
    if str(contenttype) == 'comment':
        # build list of unique users within comment list.
        users = []
        for comment in queryset:
            if not comment.user in users:
                users.append(comment.user)

    if str(contenttype) == 'contact':
        # build list of unique users from contact list.
        users = []
        for c in queryset:
            if c.user and c.user not in users:
                users.append(c.user)
    if not users:
        # we haven't built out a content-type appropriate user list.
        return HttpResponse("Error finding content type: {}".format(contenttype))

    if 'apply_blacklist' in request.POST:  # we're returning from the intermediate page and are ready to do some work.
        form = BlacklistForm(request.POST)
        if form.is_valid():
            reason  = form.cleaned_data['reason']
            spammer = form.cleaned_data['is_spammer']
            for user in users:
                # Deactivate user accounts
                # Note: Update is more efficient,
                # but we can't use it because we may have a list (from comments)
                # rather than a proper queryset.
                user.is_active = False
                user.save()

                for c in user.comment_comments.all():            # remove their comments from public view.
                    if spammer:
                        c.delete()
                    else:
                        c.is_public = False
                        c.is_removed = True
                        c.save()
                for c in user.contact_set.all():                 # and contact messages
                    if spammer:
                        c.delete()
                    else:
                        c.publish = False
                        c.save()
                # remove their session.  -- Is there a more efficient way than looping through all sessions? That can become a mighty big table.
                for s in Session.objects.all():
                    decoded_session = s.get_decoded()
                    if '_auth_user_id' in decoded_session and decoded_session['_auth_user_id'] == user.id:
                        s.delete()
                # and add them to the blacklist
                blacklist = Blacklist(
                    user        = user,
                    blacklister = request.user,
                    reason      = reason,
                )
                blacklist.save()

                if spammer:
                    resp_str = 'Any related accounts will still be visible, but related comments have been deleted.'
                else:
                    resp_str = 'Any related accounts and comments will still be visible in the admin.'

                count = len(users)
                if count == 1:
                    modeladmin.message_user(request, "{} was removed and blocked from the site. {}".format(users[0].username, resp_str))
                else:
                    modeladmin.message_user(request, "{} users were removed and blocked from the site. {}".format(count, resp_str))
            return HttpResponseRedirect(request.get_full_path())
        else:
            return HttpResponse("error!")
    # We haven't captured intermediate page data. Go there...
    return render(request, 'admin/blacklist.html', {'users': users, 'form': form})
nuke_users.short_description = "Blacklist Users"
