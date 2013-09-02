from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe

from autotagger.models import AutoTag

def autotag(content_object, text):
    """
    Takes a given block of text and tags it according to models and fields defined in settings:
    
    AUTOTAG_CONTENT = (
      {
        'model'      : 'schools.school',
        'field'      : 'school',                
        'check'      : 'is_active',               
        'm2m_field'  : 'articles',
        'reverse_m2m': 'politicians',
       },
       ... etc ...
    )
    
    THE FIELDS...
    model: 
        the app and model to check
    field:
        the particular field/value you are matching in the text
    check:
        an optional field to filter by. Maybe. If we can figure out how to do it...
    m2m_field:
        Optional. Will add the current object to a m2m field on the remote object.
        For example, if you are auto_tagging schools in articles
        you can add the article to the schools "articles" field.
    reverse_m2m:
        Optional. Will add the remote object to a m2m field on the current object.
        For example, politicians can be a m2m on articles in some cases.
        If you were tagging politicians in articles, this would add the politician
        to the article's  "politicians" field.
        
    Do NOT attempt to use both m2m and reverse_m2m on the same thing.
    """
    try:
        tag_settings = settings.AUTOTAG_CONTENT
    except:
        # print "unable to get settings"
        return text
        #return "Tag settings have not been defined. "

    #print "have tag settings, attempting to tag"
    for item in tag_settings:
        #print item
        # make sure this thing is actually an installed app
        app_label     = item['model'].split('.')[0]
        model_name    = item['model'].split('.')[1]
        field_name    = item['field']
        # this try/except may be a bad idea. Maybe we WANT it to blow up.
        try:
            # model is what we're autotagging against (politicians, schools, etc)
            # field is the field we're checking (name, etc)
            content_type = ContentType.objects.get(app_label=app_label, model=model_name)
            model        = content_type.model_class()
            field        = model._meta.get_field(field_name)
            if 'm2m_field' in item:
                m2m_field  =  model._meta.get_field(item['m2m_field'])
            else:
                m2m_field = None
            objects = model.objects.all()

            for obj in objects:
                value = getattr(obj, field.name)     # get the value from the field name
                if m2m_field:
                    m2m_values = getattr(obj, m2m_field.name)
                else:
                    m2m_values = None
                if not value:
                    continue
                # add spaces to avoid partial word matches.
                # note: this totally hoses value match before comma and at end of sentence,
                # but I'm not sure what to do about it.
                checkvalues = [' {} '.format(value), ' {}, '.format(value), ' {}.'.format(value)]
                # print checkvalues
                matched = False
                for checkvalue in checkvalues:
                    if checkvalue in text and matched == False:   # Make sure it's in there, and not done already
                        replacement = '<a href="{}" title="More on {}">{}</a>'.format(obj.get_absolute_url(), value, value)
                        text = text.replace(value, replacement, 1)
                        matched = True
                        #print text
                        if m2m_values:
                            #print "attempting to establish m2m relationship"
                            m2m_values.add(content_object)
                            #print 'established m2m'
                        if 'reverse_m2m' in item:
                            #print 'attempting reverse m2m'
                            reverse_m2m = content_object.get_field(item['reverse_m2m'])
                            reverse_m2m_values = getattr(content_object, reverse_m2m.name)
                            reverse_m2m_values.add(obj)
                            #print 'established reverse m2m'
        except Exception as error:
            return "Error: {}".format(error)

    # now do the phrases defined in autotagger models
    for tag in AutoTag.objects.all():
        # print tag.phrase
        if tag.phrase in text and content_object._meta.app_label == 'articles':
            tag.articles.add(content_object.id)
            if tag.content_object:  # since we have a content object, go ahead and link over to it.
                try:  # wrapped in case get_absolute_url doesn't exist.
                    replacement = '<a href="{}" title="More on {}">{}</a>'.format(tag.content_object.get_absolute_url(), tag.phrase, tag.phrase)
                    text = text.replace(tag.phrase, replacement, 1)
                except:
                    pass
    return mark_safe(text)
