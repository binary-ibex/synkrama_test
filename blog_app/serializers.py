from rest_framework import serializers
from .models import BlogPost, Tag
from django.contrib.auth.models import User

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag 
        fields = ['id', 'name']

class AuthorDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class AuthorShortDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username',]


class BlogPostListSerializer(serializers.ModelSerializer):
    body = serializers.SerializerMethodField()
    author = AuthorShortDetailSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True) 
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'body', 'author', 'tags', 'created_on', 'updated_on']

    def get_body(self, obj):
        return obj.body[:50] if obj.body else ""


class BlogPostDetailSerializer(serializers.ModelSerializer):
    author = AuthorDetailSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)


    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'body', 'author', 'tags', 'created_on', 'updated_on']

class BlogPostCreateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(required=True)

    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'created_on', 'updated_on', 'tags']
    
    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        instance = BlogPost.objects.create(**validated_data)

        tag_list = []
        for i in tags:
            tag = Tag.objects.filter(id=i).first()
            if tag:
                tag_list.append(tag)
        instance.tags.set(tag_list)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        
        tag_list = []
        for i in tags:
            tag = Tag.objects.filter(id=i).first()
            if tag:
                tag_list.append(tag)
        instance.tags.set(tag_list)
        instance.save()
        return instance        





