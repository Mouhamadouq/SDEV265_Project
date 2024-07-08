from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Upvote, Downvote
from django.contrib.auth import login, authenticate
from .forms import PostForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

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

@login_required
def upvote_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if not Upvote.objects.filter(post=post, user=request.user).exists():
        Upvote.objects.create(post=post, user=request.user)
    return redirect('post_list')

@login_required
def downvote_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if not Downvote.objects.filter(post=post, user=request.user).exists():
        Downvote.objects.create(post=post, user=request.user)
    return redirect('post_list')

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
