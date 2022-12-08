from api.serializers import FollowSerializer, UserDetailSerializer
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from users.models import User

class UserListViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class FollowListViewSet(ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    search_fields = (
        'user__username',
        'following__username',
    )

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user.username)
        return user.follower
