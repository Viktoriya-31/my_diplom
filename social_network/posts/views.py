from django.shortcuts import render
from django.template.context_processors import request
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(ModelViewSet):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    """
    Эндпоинты:
    - GET    /posts/           — список постов с полем likes_count
    - POST   /posts/           — создать (только авторизованные)
    - GET    /posts/{id}/      — детали поста
    - PUT/PATCH/DELETE /posts/{id}/ — редактировать/удалять (только автор)
    - POST   /posts/{id}/like/   — поставить лайк (только авторизованные)
    - DELETE /posts/{id}/unlike/ — снять лайк (только авторизованные)
    """

    queryset = Post.objects.annotate(likes_count = Count('likes')).order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author = self.request.user)


    @action(detail=True, methods = ['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk = None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(
            post=post,
            user=request.user
        )
        if not created:
            return Response(
                {'detail': 'Вы уже лайкнули этот пост.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'likes_count': post.likes.count()},
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        try:
            like = Like.objects.get(post=post, user=request.user)
            like.delete()
            return Response(
                {'likes_count': post.likes.count()},
                status=status.HTTP_204_NO_CONTENT
            )
        except Like.DoesNotExist:
            return Response(
                {'detail': 'Вы не ставили лайк этому посту.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class CommentViewSet(ModelViewSet):

    """
    Эндпоинты:
    - GET    /comments/         — все комментарии или фильтр по ?post=<id>
    - POST   /comments/         — оставить комментарий (только авторизованные)
    - GET    /comments/{id}/    — детали
    - PUT/PATCH/DELETE /comments/{id}/ — редактировать/удалять (только автор)
    """

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.order_by('created_at')
        post_id = self.request.query_params.get('post')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author = self.request.user)
