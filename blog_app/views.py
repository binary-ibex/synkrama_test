from rest_framework import generics, status
from blog_app.filters import BlogPostAuthorFilterBackend, BlogPostSearchFilterBackend, BlogPostTagFilterBackend, TagSearchFilterBackend
from blog_app.serializers import BlogPostCreateSerializer, BlogPostDetailSerializer, BlogPostListSerializer, TagSerializer
from .models import BlogPost, Tag
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class BlogPostView(generics.GenericAPIView):
    queryset = BlogPost.objects.filter(is_deleted=False).order_by('-created_on')
    permission_classes = [IsAuthenticated]
    serializer_class = BlogPostDetailSerializer
    filter_backends = [BlogPostTagFilterBackend, BlogPostAuthorFilterBackend, BlogPostSearchFilterBackend]
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            instance = self.get_object()
            serializer = self.get_serializer(instance)
        else:
            queryset = self.get_queryset()
            queryset = self.filter_queryset(queryset)
            serializer = BlogPostListSerializer(queryset, many=True)
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    def post(self, request, *args, **kwargs):
        serializer = BlogPostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['author'] = request.user
            instance = serializer.create(serializer.validated_data)
            response_data = {'data': self.get_serializer(instance).data}
            status_code = status.HTTP_201_CREATED
        else:
            response_data = {'detail': "Invalid Payload"}
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(
            status=status_code,
            data=response_data
        )

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if request.user == instance.author or request.user.is_superuser:
            if serializer.is_valid():
                instance = serializer.update(
                    instance, serializer.validated_data)
                response_message = self.get_serializer(instance).data
                status_code = status.HTTP_200_OK
            else:
                response_message = {"detail": "Invalid payload"}
                status_code = status.HTTP_400_BAD_REQUEST
        else:
            response_message = {
                "detail": "User don't have permission to update post"}
            status_code = status.HTTP_403_FORBIDDEN
        return Response(
            status=status_code,
            data=response_message
        )

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        # if user is not superuser then allow only deleteing post created byt the user
        if request.user == instance.author or request.user.is_superuser:
            instance.is_deleted = True
            instance.save()
            response_message = "Data deleted succesfully"
            status_code = status.HTTP_200_OK
        else:
            response_message = "Not allow to delete post"
            status_code = status.HTTP_403_FORBIDDEN

        return Response(
            data={
                'message': response_message
            },
            status=status_code
        )


class TagView(generics.GenericAPIView):
    queryset = Tag.objects.order_by('-id')
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer
    filter_backends = [TagSearchFilterBackend]
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            instance = self.get_object()
            searilizer = self.get_serializer(instance)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            searilizer = self.get_serializer(queryset, many=True)
        return Response(
            status=status.HTTP_200_OK,
            data={'data':searilizer.data}
        )

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            response_message = {
                "detail": "User don't have permission to update post"}
            status_code = status.HTTP_403_FORBIDDEN
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.create(serializer.validated_data)
            response_message = self.get_serializer(instance).data
            status_code = status.HTTP_200_OK
        else:
            response_message = {"detail": "Invalid payload"}
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(
            status=status_code,
            data=response_message
        )

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            instance = serializer.update(instance, serializer.validated_data)
            response_message = self.get_serializer(instance).data
            status_code = status.HTTP_200_OK
        else:
            response_message = {"detail": "Invalid payload"}
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(
            status=status_code,
            data=response_message
        )

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        response_message = "Data deleted succesfully"
        status_code = status.HTTP_200_OK

        return Response(
            data={
                'message': response_message
            },
            status=status_code
        )
