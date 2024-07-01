from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
    path('post/<int:post_id>/upvote/', views.upvote_post, name='upvote_post'),
    path('post/<int:post_id>/downvote/', views.downvote_post, name='downvote_post'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
