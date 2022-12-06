from api.views import UserGetTokenView, UserRegistrationView, UserViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', UserRegistrationView.as_view(), name='signup'),
    path('auth/token/', UserGetTokenView.as_view(), name='token')
]
