from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=2000)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False)
    tags = models.ManyToManyField(to='Tag', related_name="tag_posts")
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name
    
class BlockUser(models.Model):
    block_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='block_user_user')
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='author_user')
    