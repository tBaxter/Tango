from django import forms


class TextCounterWidget(forms.Textarea):
    """
    Used for textAreas that need to count their characters
    """
    class Media:
        js = ('/static/admin/text_field_counter.js',)

    def render(self, name, value, attrs=None):
        if attrs:
            attrs['data-counter'] = 'needs_counter'
        else:
            attrs = {'data-counter': 'needs_counter'}
        return super(TextCounterWidget, self).render(name, value, attrs)
