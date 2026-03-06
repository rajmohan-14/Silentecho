from django.urls import path
from . import views

urlpatterns = [
    path('',              views.feed,        name='feed'),
    path('submit/',       views.submit_post, name='submit_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
]