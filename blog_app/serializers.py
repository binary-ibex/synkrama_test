from rest_framework import serializers
from .models import Author, BlogPost
from django.contrib.auth.models import User


class AuthorDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['username', 'email', 'first_name', 'last_name']


class BlogPostListSerializer(serializers.ModelSerializer):
    body = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'body','created_on', 'updated_on']

    def get_body(self, obj):
        return obj.body[:50] if obj.body else ""


class BlogPostDetailSerializer(serializers.ModelSerializer):
    author = AuthorDetailSerializer(read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'body', 'author', 'created_on', 'updated_on']

class BlogPostCreateSerializer(serializers.ModelSerializer):
    author = AuthorDetailSerializer

    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'author', 'created_on', 'updated_on']
