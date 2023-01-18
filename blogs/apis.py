from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from blogs.models import Blog


def get_like(request: HttpRequest, blog_id: int):
    if request.method != "GET":
        return redirect(reverse("blogs:detail", kwargs={"pk": blog_id}))

    blog = get_object_or_404(Blog, pk=blog_id)
    is_liked = blog.likes.filter(id=request.user.id).exists()
    return JsonResponse({"is_liked": is_liked})


def toggle_like(request: HttpRequest, blog_id: int):
    """toggle_like
    when logged-in user touch like button in blogs/detail.html,
    toggle Blog.likes

    Args:
        request: HttpRequest - GET Method
        blog_id: int - blog.id

    Returns:
        JsonResponse: return num of likes
    """
    if request.method != "GET":
        return redirect(reverse("blogs:detail", kwargs={"pk": blog_id}))

    blog = get_object_or_404(Blog, pk=blog_id)
    if blog.likes.filter(id=request.user.id).exists():
        # when you already like this blog, remove like
        blog.likes.remove(request.user)
    else:
        # still not, add like
        blog.likes.add(request.user)

    return JsonResponse({"like_count": blog.likes.count()})
