from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from .models import Post, Group
from .forms import PostForm

User = get_user_model()

def index(request):
    keyword = request.GET.get("query", None)
    page_number = request.GET.get('page', 1)
    if keyword:
        posts_list = Post.objects.select_related("author", "group").all().filter(text__contains = keyword)
    else:
        posts_list = Post.objects.select_related("author", "group").all()
    paginator = Paginator(posts_list, 4)
    
    page = paginator.get_page(page_number)
    
    return render(request, "index.html", {"page": page})

def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    latest = group.posts.all()[:10]
    return render(request, "group.html", {"group":group,"posts": latest})

@login_required
def new_post(request):    
    form = PostForm(request.POST or None)
    if(request.method == 'POST' and form.is_valid):
        post = form.save(commit=False) 
        post.author = request.user 
        form.save() 
        return redirect('profile', username = request.user)
    return render(request, "new-post.html", {"form": form,})

def profile(request, username):
    author = get_object_or_404(User, username=username)

    page_number = request.GET.get('page', 1)
    posts_list = author.posts.all() 
    paginator = Paginator(posts_list, 4)
    page = paginator.get_page(page_number)

    count = Post.objects.filter(author=author).count()
    context = {
        "author": author,
        "page": page,
        "post_count": count,
    }
    return render(request, 'profile.html', context)

def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username) 
    post = get_object_or_404(Post, id = post_id, author = author)
    post_count = Post.objects.filter(author=author).count()
    context = {
        "post": post,
        "post_count": post_count,
    }
    return render(request, 'post.html', context)    

@login_required
def post_edit(request, username, post_id):
    author = get_object_or_404(User, username=username) 
    post = get_object_or_404(Post, author=author, id=post_id)
    form = PostForm(request.POST or None, instance=post)
    
    if request.user != author:
        return redirect('post', username = username, post_id=post_id)
    
    if(request.method == 'POST' and form.is_valid):
        post = form.save(commit=False) 
        post.author = request.user 
        form.save() 
        return redirect('post', username = request.user, post_id = post_id)
    context = {
        'form': form, 
        'post': post,
    }
    return render(request, "new-post.html", context)   