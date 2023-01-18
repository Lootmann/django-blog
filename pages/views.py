from django.views import generic

from blogs.models import Blog


class PagesIndexView(generic.ListView):
    template_name = "pages/index.html"
    model = Blog
    context_object_name = "blogs"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blogs"] = Blog.objects.all()
        return context
