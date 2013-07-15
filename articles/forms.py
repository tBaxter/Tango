from django.forms import ModelForm, HiddenInput, FileField, FileInput

from .models import Article, ArticleImage


class BlogEntryForm(ModelForm):  # for adding and editing entries
    upload = FileField(
        required=False,
        label = "Upload your file(s)",
        help_text='You can upload one or more JPG files.',
        widget=FileInput(attrs={'multiple': 'multiple'})
    )

    class Meta:
        model = Article
        fields = (
            'title',
            'summary',
            'body',
            'upload'
        )


class BlogEntryImageForm(ModelForm):
    class Meta:
        model = ArticleImage
        fields = ('image', 'caption', 'article', 'byline')
        widgets = {
            'article': HiddenInput(),
            'byline':  HiddenInput()
        }
