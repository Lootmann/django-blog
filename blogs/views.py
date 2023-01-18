from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from blogs.forms import BlogCreateForm, BlogUpdateForm
from blogs.models import Blog


class BlogIndexView(generic.ListView):
    """BlogIndexView
    BlogIndexView (/blogs/) shows only current logged in user's blog
    """

    template_name = "blogs/index.html"
    model = Blog
    context_object_name = "blogs"

    def get_queryset(self):
        queryset = super(BlogIndexView, self).get_queryset()
        return queryset.filter(author=self.request.user)


class BlogCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "blogs/create.html"
    model = Blog
    form_class = BlogCreateForm
    success_url = reverse_lazy("blogs:index")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "blogs/detail.html"
    model = Blog
    context_object_name = "blog"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = get_object_or_404(Blog, id=self.kwargs["pk"])
        context["is_liked"] = blog.likes.filter(id=self.request.user.id).exists()
        context["like_count"] = blog.likes.all().count()
        return context

    def get(self, request, *args, **kwargs):
        # NOTE: I don't know how to use dispatch correctly :^)
        blog = Blog.objects.get(pk=kwargs["pk"])
        blog.clicked_count += 1
        blog.save()
        return super().get(request, *args, **kwargs)


class BlogUpdateView(LoginRequiredMixin, generic.View):
    template_name = "blogs/update.html"
    model = Blog
    form_class = BlogUpdateForm

    def get(self, request, *args, **kwargs):
        # when Blog.pk == kwargs["pk"] is not found,
        # redirects 404.html page.
        blog = get_object_or_404(Blog, pk=kwargs["pk"])

        # Check whether requested user has permission.
        # This permission means request user == blog.author
        if request.user != blog.author:
            raise Http404("Something Wrong With D:")

        form = self.form_class(instance=blog)
        title = blog.title
        return render(request, self.template_name, {"form": form, "title": title})

    def post(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=kwargs["pk"])

        if request.user != blog.author:
            raise Http404("Something Wrong With D:")

        # when updated form, you must use this expression
        form = self.form_class(request.POST, instance=blog)

        if form.is_valid():
            updated_blog = form.save(commit=False)
            updated_blog.author = blog.author
            updated_blog.save()
            return redirect(reverse("blogs:detail", kwargs={"pk": blog.id}))
        else:
            return render(request, self.template_name, {"form": form})


class BlogDeleteView(LoginRequiredMixin, generic.View):
    template_name = "blogs/delete.html"
    model = Blog
    context_object_name = "blog"

    def get(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=kwargs["pk"])

        if request.user != blog.author:
            raise Http404("Something Wrong With D:")

        return render(request, self.template_name, {"blog": blog})

    def post(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=kwargs["pk"])

        if request.user != blog.author:
            raise Http404("Something Wrong With D:")

        blog.delete()

        return redirect(reverse("blogs:index"))
