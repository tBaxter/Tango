import datetime
import time

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView, ListView, UpdateView, CreateView

from .models import Article, ArticleImage, Destination
from .forms import BlogEntryForm, BlogEntryImageForm

now = datetime.datetime.now()
pagination_setting = getattr(settings, "PAGINATE_BY", 25)


class DestinationList(ListView):
    """
    Returns a list of article/blog destinations
    """
    template_name = 'articles/index.html'
    paginate_by = pagination_setting
    model = Destination
destination_list = DestinationList.as_view()


class ArticleList(ListView):
    """
    Returns an article list, plus the related destination.
    """
    template_name = 'all_content/article_list.html'
    paginate_by = pagination_setting
    destination = None

    def dispatch(self, request, *args, **kwargs):
        self.destination_slug = kwargs.get('destination_slug', None)
        if self.destination_slug:
            self.destination = Destination.objects.get(slug=self.destination_slug)
        return super(ArticleList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.destination:
            return Article.published.filter(destination=self.destination)
        return Article.published.all()

    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        context['destination'] = self.destination
        return context
article_list = ArticleList.as_view()


class ArticleDetail(DetailView):
    """
    Returns an article detail, plus its parent destination.

    """
    template_name = 'all_content/article_detail.html'
    queryset = Article.published.all()

    def dispatch(self, request, *args, **kwargs):
        self.destination_slug = kwargs.get('destination_slug', False)
        return super(ArticleDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        if self.destination_slug:
            obj = self.get_object()
            created = obj.created
            context['destination'] = obj.destination
            valid_articles = Article.published.filter(destination__slug=self.destination_slug)
            try:
                next_update = valid_articles.filter(created__gt=created)[0]
            except IndexError:
                next_update = None
            try:
                prev_update = valid_articles.filter(created__lt=created).order_by('-created')[0]
            except IndexError:
                prev_update = None
            context.update({
                'next_update' : next_update,
                'prev_update' : prev_update
            })
        return context
article_detail = ArticleDetail.as_view()


@never_cache
def add_image(request, destination_slug, entry_slug):
    entry = Article.objects.get(slug=entry_slug)
    if request.user != entry.destination.author:
        return HttpResponse("""
            You can't add pictures to this content.
            Make sure you are logged in and have been given the proper permissions.
            """)
    form = BlogEntryImageForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/blogs/entry/thank-you/')
    return render(request, 'blogs/add_image.html', {'form': form})


def edit_entry(request, blog_slug, object_id):
    if request.method == 'POST':
        entry = Article.objects.get(id=object_id)
        entry.body = request.POST['body']
        entry.save()
        return HttpResponse(str(entry.body))
    return UpdateView(
        form_class=BlogEntryForm,
        object_id=object_id,
        login_required=True,
        template_name="blogs/add_entry.html",
    )


class CreateBlogEntry(CreateView):
    form_class = BlogEntryForm
    model = Article
    template_name = "blogs/entry_form.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.destination = Destination.objects.get(slug=kwargs.get('destination_slug'))
        if not request.user.has_perm('can_add_article'):
            return HttpResponse(
                """
                You do not appear to be a blogger.
                Make sure you are logged in and have been given the proper permissions.
                """
            )
        if request.user != self.destination.author:
            return HttpResponse(
                """
                You do not appear to be the designated author.
                Make sure you are logged in and have been given the proper permissions.
                """
            )
        return super(CreateBlogEntry, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        self.obj.destination = self.destination
        self.obj.slug = slugify(self.obj.title)
        self.obj.author = self.request.user
        self.obj.save()
        for upload_file in self.request.FILES.getlist('upload'):
            new_image = ArticleImage(
                article = self.obj,
                image = upload_file
            )
            new_image.save()
        messages.success(self.request, 'Your entry has been added')
        return HttpResponseRedirect(reverse('blog_entry_detail', args=(self.destination.slug, self.obj.slug)))


class EditBlogEntry(UpdateView):
    form_class = BlogEntryForm
    model = Article
    template_name = "blogs/entry_form.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditBlogEntry, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.id != self.object.author.id:
            messages.error(request, 'You do not have permission to edit this.')
            url = reverse('blog_entry_detail', args=(self.destination.slug, self.object.slug))
            return HttpResponseRedirect(url)
        return super(EditBlogEntry, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        self.obj = form.save()
        process_upload(self.request.FILES.getlist('upload'), form, self.obj, self.request.user)
        messages.success(self.request, 'Your entry has been edited')
        return HttpResponseRedirect(reverse('blog_entry_detail', args=(self.destination.slug, self.obj.slug)))


def process_upload(photo_list, form, parent_object, user, status=''):
    """
    Helper function that actually processes and saves the upload(s).
    Segregated out for readability.
    """
    status += "beginning upload processing. Gathering and normalizing fields....<br>"

    for upload_file in photo_list:
        # lowercase and replace spaces in filename
        upload_file.name = upload_file.name.lower().replace(' ', '_')
        upload_name = upload_file.name

        status += "File is %s. Checking for single file upload or bulk upload... <br>" % upload_name
        if upload_name.endswith('.jpg') or upload_name.endswith('.jpeg'):
            status += "Found jpg. Attempting to save... <br>"
            try:
                dupe = ArticleImage.objects.get(photo__contains=upload_name, article=parent_object)
            except:
                dupe = None
            if not dupe:
                try:
                    upload = ArticleImage(
                        article = parent_object,
                        photo = upload_file
                    )
                    upload.save()
                    status += "Saved and uploaded jpg."
                except Exception, inst:
                    status += "Error saving image: %s" % (inst)
        time.sleep(1)
    return status
