from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.query import QuerySet
from django.utils import timezone


class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "admin"
        AUTHOR = "AUTHOR", "author"

    base_role = Role.ADMIN
    role = models.CharField(max_length=100, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)


class Author(User):
    base_role = User.Role.AUTHOR

    class Meta:
        proxy = True


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=2000)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE, null=False)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.title
