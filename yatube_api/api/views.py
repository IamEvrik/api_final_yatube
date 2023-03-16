"""Вьюсеты для api."""

from rest_framework import filters, mixins, pagination, permissions, viewsets

from django.shortcuts import get_object_or_404

from api.permissions import IsOwnerOrReadOnly
from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from posts.models import Group, Post


class CreateListViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet
):
    """Доступно только создание и получение списка."""


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Отображение сообществ."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Отображение публикаций."""

    queryset = Post.objects.select_related('author')
    serializer_class = PostSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    )

    def perform_create(self, serializer):
        """Автор публикации добавляется при сохранении."""
        return serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Отображение комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    )

    def get_queryset(self):
        """Подбор комментариев к указанной публикации."""
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.select_related('author')

    def perform_create(self, serializer):
        """При сохранении комментария добавляется код публикации и автор."""
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return serializer.save(author=self.request.user, post=post)


class FollowViewSet(CreateListViewSet):
    """Отображение подписок."""

    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Выборка подписок текущего пользователя."""
        return self.request.user.followings.select_related('user')

    def perform_create(self, serializer):
        """При сохранении добавляется пользователь."""
        return serializer.save(user=self.request.user)
