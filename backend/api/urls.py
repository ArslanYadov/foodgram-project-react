from api.views import FollowListViewSet, UserListViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserListViewSet, basename='users')

urlpatterns = [
    path('users/subscriptions/', FollowListViewSet.as_view(), name='subscriptions'),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
