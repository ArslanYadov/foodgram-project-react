from rest_framework import status
from rest_framework.test import APITestCase
from recipes.models import Tag


class UserUrlTests(APITestCase):
    """Класс тестов доступности URL адресов."""
    def setUp(self):
        self.tag_url = 'http://testserver/api/tags/'

    def test_tag_url(self):
        """Тест доступности URL с тэгами."""
        response = self.client.get(path=self.tag_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_exists_tag_id_url(self):
        """
        Тестируем ответ URL по тэгам,
        если они ещё не созданны.
        """
        tag_id_url = self.tag_url + '1/'
        response = self.client.get(path=tag_id_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_exists_tag_id_url(self):
        """Тестируем ответ URL по существующему id тэга."""
        tag_data = {
            'name': 'завтрак',
            'color': '#E26C2D',
            'slug': 'breakfast'
        }
        tag = Tag.objects.create(**tag_data)
        
        tag_id_url = self.tag_url + str(tag.id) + '/'
        response = self.client.get(path=tag_id_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
