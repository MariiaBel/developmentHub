from django.shortcuts import render, get_object_or_404
from .models import Post, Group


def index(request):
    keyword = request.GET.get("query", None)
    if keyword:
        post = Post.objects.select_related("author", "group").all().filter(text__contains = keyword)
    else:
        post = None
    return render(request, "index.html", {"posts": post})

def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    latest = group.posts.all()[:10]
    return render(request, "group.html", {"group":group,"posts": latest})