from rest_framework import filters
from django.db.models import Q

from blog_app.models import BlockUser

class BlogPostSearchFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        search = request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(author__first_name__icontains=search) | Q(author__last_name__icontains=search))
        return queryset


class BlogPostAuthorFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        author_id = request.GET.get('author_id')
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        return queryset


class BlogPostTagFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        tag_list = request.GET.getlist('tag')
        if tag_list:
            queryset = queryset.filter(tags__name__in=tag_list)
        return queryset

class BlogPostBlockUserFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        login_user = request.user 
        if not login_user.is_superuser:
            blocked_by_author = BlockUser.objects.filter(block_user=login_user).distinct().values_list('author')
            if login_user:
                queryset = queryset.exclude(author__in=blocked_by_author)
        return queryset


class TagSearchFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        search = request.GET.get('search')

        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset
    

class BlockUserFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        login_user = request.user
        if login_user:
            queryset = queryset.filter(author=login_user)
        return queryset
    
