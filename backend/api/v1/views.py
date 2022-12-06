from api.v1.serializers import (
    UserGetTokenSerializer,
    UserRegistrationSerializer,
    UserSerializer
)
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from foodgram.settings import EMAIL_ROBOT
from recipes.models import User
from rest_framework.decorators import action
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRegistrationView(APIView):
    def post(self, request):
        serialiazer = UserRegistrationSerializer(data=request.data)
        if serialiazer.is_valid(raise_exception=True):
            user = serialiazer.save()
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                'Код подтверждения регистрации',
                '{}'.format(confirmation_code),
                EMAIL_ROBOT,
                [serialiazer.validated_data.get('email')]
            )
            return Response(serialiazer.data, status=status.HTTP_200_OK)


class UserGetTokenView(APIView):
    def post(self, request):
        serializer = UserGetTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get('username')
            user = get_object_or_404(User, username=username)
            token = serializer.validated_data.get('confirmation_code')
            confirmation_code = default_token_generator.check_token(
                user, token
            )
            if not confirmation_code:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            refresh = RefreshToken.for_user(user)
            return Response(
                {'token': str(refresh.access_token)},
                status=status.HTTP_200_OK
            )
