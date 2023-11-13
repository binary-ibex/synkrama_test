from rest_framework import generics, status
from blog_app.serializers import BlogPostCreateSerializer, BlogPostDetailSerializer, BlogPostListSerializer
from .models import BlogPost
from rest_framework.response import Response


class BlogPostView(generics.GenericAPIView):
    queryset = BlogPost.objects.order_by('-created_on')
    serializer_class = BlogPostDetailSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            instance = self.get_object()
            response_json = self.get_serializer(instance).data
        else:
            queryset = self.get_queryset().filter(is_deleted=False)
            response_json = BlogPostListSerializer(queryset, many=True).data
        return Response(
            status=status.HTTP_200_OK,
            data = response_json
            )

    def post(self, request, *args, **kwargs):
        serializer = BlogPostCreateSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.create(serializer.validated_data)
            response_json = self.get_serializer(instance).data
        return Response(
            status=status.HTTP_201_CREATED,
            data = response_json
        )

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.update(instance, serializer.validated_data)
            response_json = self.get_serializer(instance).data
        return Response(
            status=status.HTTP_200_OK,
            data = response_json
            )

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(
            data = {
                'message': "Data deleted succesfully"
            },
            status=status.HTTP_200_OK
        )
