from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
    path('post/<int:post_id>/upvote/', views.upvote_post, name='upvote_post'),
    path('post/<int:post_id>/downvote/', views.downvote_post, name='downvote_post'),
]
