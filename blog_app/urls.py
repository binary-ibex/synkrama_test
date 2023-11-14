from django.urls import path
from .views import *

urlpatterns = [
    path('posts', BlogPostView.as_view(), name='blog_post_view'),
    path('posts/<int:pk>', BlogPostView.as_view(), name='blog_post_view'),
    path('tags', TagView.as_view(), name='tag_view'),
    path('tags/<int:pk>', TagView.as_view(), name='tag_view'),
    path('get-blocked-user', BlockUserView.as_view(), name='get_block_user_view'),
    path('block-user', BlockUnblockUserView.as_view(), name='block_unblock_user_view'),
    path('block-user/<int:pk>', BlockUnblockUserView.as_view(), name='block_unblock_user_view'),
]