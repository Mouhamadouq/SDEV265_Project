from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Post, Upvote, Downvote

def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'blog/post_list.html', context)

def author_detail(request, author_id):
    author = get_object_or_404(User, pk=author_id)
    posts = Post.objects.filter(author=author)
    context = {
        'author': author,
        'posts': posts
    }
    return render(request, 'blog/author_detail.html', context)

def upvote_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if not Upvote.objects.filter(post=post, user=request.user).exists():
        Upvote.objects.create(post=post, user=request.user)
    
    return render(request, 'blog/post_list.html', {'post': post})

def downvote_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if not Downvote.objects.filter(post=post, user=request.user).exists():
        Downvote.objects.create(post=post, user=request.user)
    
    return render(request, 'blog/post_list.html', {'post': post})