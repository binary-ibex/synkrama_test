from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import BlockUser, BlogPost, Tag
from django.contrib.auth.models import User


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name']


class AuthorDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UserShortDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username',]


class BlogPostListSerializer(serializers.ModelSerializer):
    body = serializers.SerializerMethodField()
    author = UserShortDetailSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'body', 'author',
                  'tags', 'created_on', 'updated_on']

    def get_body(self, obj):
        return obj.body[:50] if obj.body else ""


class BlogPostDetailSerializer(serializers.ModelSerializer):
    author = AuthorDetailSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'body', 'author',
                  'tags', 'created_on', 'updated_on']


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


class BlockUserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    author = UserShortDetailSerializer(read_only=True)
    block_user = UserShortDetailSerializer(read_only=True)

    class Meta:
        model = BlockUser
        fields = ['id', 'author', 'block_user']


class BlockUnblockUserSerializer(serializers.ModelSerializer):
    block_user = serializers.CharField(required=True)

    class Meta:
        model = BlockUser
        fields = ['block_user']

    def create(self, validated_data):
        block_user_id = validated_data.pop('block_user')
        validated_data['block_user'] = User.objects.get(id=block_user_id)

        if validated_data['block_user'] == validated_data['author']:
            raise ValidationError(detail={"detail": "Invalid data"})

        instance = BlockUser.objects.filter(
            author=validated_data['author'], block_user=validated_data['block_user']).first()

        if not instance:
            instance = BlockUser.objects.create(**validated_data)
        
        return instance
