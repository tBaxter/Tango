from django.views.generic import ListView, TemplateView, DetailView


class ContextListView(ListView):
    """ Allows passing extra_context through list view. """
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ContextListView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


class ContextTemplateView(TemplateView):
    """ Allows passing extra_context through template view. """
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ContextTemplateView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


class ContextDetailView(DetailView):
    """ Allows passing extra_context through detail view. """
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ContextDetailView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context
