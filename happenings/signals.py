def update_time(sender, **kwargs):
    """
    When a Comment is added, updates the Update to set "last_updated" time
    """
    comment = kwargs['instance']
    if comment.content_type.app_label == "happenings" and comment.content_type.name=="Update":
       from happenings.models import Update
       item=Update.objects.get(id=comment.object_pk)
       item.save()