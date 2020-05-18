from django.shortcuts import render, get_object_or_404
from .models import Post


def blog(request):
    posts = Post.objects.all().order_by("-posted_at")
    return render(request, "website/blog.html", {"posts": posts})


def blog_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, "website/blog-detail.html", {"post": post})

