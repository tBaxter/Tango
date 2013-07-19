from django.contrib import admin
from voting.models import Vote


class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'vote')

admin.site.register(Vote, VoteAdmin)
