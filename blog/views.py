from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Upvote, Downvote
from django.contrib.auth import login, authenticate

def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'blog/post_list.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('post_list')
        else:
            print(form.errors)  # Debugging: print form errors
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def home(request):
    return render(request, 'blog/post_list.html')


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