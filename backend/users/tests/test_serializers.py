import random
from django.urls import include, path, reverse
from foodgram.settings import RESERVED_USERNAME_LIST
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase, URLPatternsTestCase
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

    def _registrate_user(self):
        """Регистрация пользователя."""
        return self.client.post(path=reverse('user-list'), data=self.user_info, format='json')
    
    def _login_user(self):
        """Авторизация пользователя."""
        self._registrate_user()
        return self.client.post(path=reverse('login'), data=self.user_info, format='json')

    def test_registration_user(self):
        """Проверяем создания пользователя после регистрации."""
        response = self._registrate_user()
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
    
    def test_registration_user_with_reserved_username(self):
        """Проверка регистрации пользователя по зарезервированному имени."""
        url = reverse('user-list')
        self.user_info['username'] = random.choice(RESERVED_USERNAME_LIST)
        response = self.client.post(url, data=self.user_info, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.json()
        self.assertEqual('Данное имя зарезервированно!', *data.get('username'))
        self.assertEqual(User.objects.count(), 0)

    def test_login_user(self):
        """
        Проверка пользователь может авторизироваться.
        При авторизации для пользователя создается токен.
        """
        self._registrate_user()
        response = self._login_user()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Token.objects.count(), 1)
        token = Token.objects.first()
        self.assertEqual(response.json().get('auth_token'), token.key)

    def test_logout_user(self):
        """
        Проверяем, что когда пользователь разлогинулся, токен удаляется.
        """
        self._login_user()
        token = Token.objects.first()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.client.post(path=reverse('logout'), format='json')

        self.assertEqual(Token.objects.count(), 0)


    def test_non_authenticated_user_change_password(self):
        """Тест смены пароля не авторизованным пользователем."""
        url = 'http://testserver/api/users/set_password/'
        respone = self.client.post(path=url, data=self.user_info, format='json')
        self.assertEqual(respone.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_is_authenticated_user_change_password(self):
        """Тест смены пароля авторизованным пользователем."""
        url = 'http://testserver/api/users/set_password/'
        self._login_user()
        old_password = User.objects.first().password
        token = Token.objects.first()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            'new_password': 'b3$t_P4ssw0RD',
            'current_password': self.user_info.get('password')
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        new_password = User.objects.first().password
        self.assertNotEqual(old_password, new_password)

    def test_endpoint_me(self):
        """
        Тестим, что эндпоинт users/me/
        отдает информация о текущем пользователе.
        """
        self._login_user()
        token = Token.objects.first()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        user = User.objects.first()

        response = self.client.get(path='http://testserver/api/users/me/')
        data = response.json()
        current_user = (
            (user.email, data.get('email')),
            (user.id, data.get('id')),
            (user.username, data.get('username')),
            (user.first_name, data.get('first_name')),
            (user.last_name, data.get('last_name')),
            (False, data.get('is_subscribed')),
        )
        for value, expected in current_user:
            with self.subTest(value=value):
                self.assertEqual(value, expected)

    def test_current_user(self):
        """
        Проверка того, что эндпоинт /users/{id}/
        отдает информацию о конкретном пользователе.
        """
        self._registrate_user()
        user = User.objects.first()
        response = self.client.get(path='http://testserver/api/users/{}/'.format(user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
