from api.serializers import UserDetailSerializer
from djoser.views import UserViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from users.models import User

class UserListViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
