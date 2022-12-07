from api.views import UserRegistrationView
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('users/', UserRegistrationView.as_view(), name='users'),
]
