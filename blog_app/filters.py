from rest_framework import filters
from django.db.models import Q

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
    

class TagSearchFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        search = request.GET.get('search')

        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset