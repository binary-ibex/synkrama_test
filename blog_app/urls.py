from django.urls import path
from .views import *

urlpatterns = [
    path('posts/<int:pk>', BlogPostView.as_view(), name='blog_post_view'),
    path('posts', BlogPostView.as_view(), name='blog_post_view'),
]