from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from users.models import User

class UserRegistrationTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('users.urls')),
    ]

    def setUp(self):
        self.user_info = {
            'first_name': 'Вася',
            'last_name': 'Пупкин',
            'username': 'noobMaster2000',
            'email': 'fake@mail.com',
            'password': 'Best_Password_12345'
        }

    def test_create_user(self):
        """Проверяем создания пользователя после регистрации."""
        url = reverse('user-list')
        response = self.client.post(url, data=self.user_info, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        new_user = User.objects.first()
        user_fields = (
            (new_user.first_name, self.user_info.get('first_name')),
            (new_user.last_name, self.user_info.get('last_name')),
            (new_user.username, self.user_info.get('username')),
            (new_user.email, self.user_info.get('email'))
        )
        for value, expected in user_fields:
            with self.subTest(value=value):
                self.assertEqual(value, expected)
