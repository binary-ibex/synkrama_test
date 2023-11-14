from django.urls import path
from .views import *

urlpatterns = [
    path('posts', BlogPostView.as_view(), name='blog_post_view'),
    path('posts/<int:pk>', BlogPostView.as_view(), name='blog_post_view'),
    path('tags', TagView.as_view(), name='tag_view'),
    path('tags/<int:pk>', TagView.as_view(), name='tag_view'),
]