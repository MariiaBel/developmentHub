from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 

from .models import Post, Group
from .forms import PostForm


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

@login_required
def new_post(request):
    if(request.method == 'POST'):
        form = PostForm(request.POST)
        if form.is_valid:
            post = form.save(commit=False) 
            post.author = request.user 
            form.save() 
            return redirect('/')
    form = PostForm()
    return render(request, "new-post.html", {"form": form})

