from django.contrib import auth
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from .models import Post, Group, Comment, Follow
from .forms import PostForm, CommentForm

User = get_user_model()

def index(request):
    keyword = request.GET.get("query", None)
    page_number = request.GET.get('page', 1)
    if keyword:
        posts_list = Post.objects.select_related("author", "group").filter(text__contains = keyword)
    else:
        posts_list = Post.objects.select_related("author", "group")
    paginator = Paginator(posts_list, 4)
    
    page = paginator.get_page(page_number)
    
    return render(request, "index.html", {"page": page})

def group_posts(request, slug):
    page_number = request.GET.get('page', 1)
    group = get_object_or_404(Group, slug=slug)
    latest = group.posts.select_related("author", "group")
    paginator = Paginator(latest, 4)    
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "group": group,
    }
    return render(request, "group.html", context)

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
    is_following = False 
    if request.user.is_authenticated: 
        is_following = Follow.objects.filter(user = request.user, author = author).exists()
    context = {
        "author": author,
        "page": page,
        "post_count": count,
        "following": is_following,
    }
    return render(request, 'profile.html', context)

def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username) 
    post = get_object_or_404(Post, id = post_id)
    post_count = Post.objects.filter(author=author).count()
    form = CommentForm(request.POST or None)
    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "post_count": post_count,
        'comments': comments,
        'form': form,
    }
    return render(request, 'post.html', context)    

@login_required
def post_edit(request, username, post_id):
    author = get_object_or_404(User, username=username)     
    if request.user != author:
        return redirect('post', username = username, post_id=post_id)

    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)    
    
    if(request.method == 'POST' and form.is_valid):
        post = form.save(commit=False) 
        post.author = request.user 
        form.save() 
        return redirect('post', username = request.user.username, post_id = post_id)

    context = {
        'form': form, 
        'post': post,
    }
    return render(request, "new-post.html", context)   

def page_not_found(request, exception):
    return render(
        request, 
        "misc/404.html", 
        {"path": request.path}, 
        status=404
    )
def server_error(request):
    return render(request, "misc/500.html", status=500)     

def add_comment(request, username, post_id): 
    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post, id = post_id)
    if(request.method == 'POST' and form.is_valid):
        comment = form.save(commit=False) 
        comment.author = request.user 
        comment.post = post
        form.save() 
    return redirect('post', username = username, post_id=post_id)  

@login_required
def follow_index(request):
    """Page for user with his/her followed author's posts"""
    post_list = Post.objects.filter(author__following__user = request.user).select_related("author", "group")
    page_number = request.GET.get('page', 1)
    paginator = Paginator(post_list, 4)    
    page = paginator.get_page(page_number)
    post_count = page.object_list.count()
    context = {  
        "page": page,
        "post_count": post_count,
    }
    return render(request, "follow.html", context)

@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    is_following = Follow.objects.filter(user = request.user, author = author).exists()
    if username != request.user.username and not is_following:
        Follow.objects.create(user = request.user, author = author)
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user = request.user, author = author).delete()
    return redirect('profile', username=username)