from rest_framework.test import APITestCase
from recipes.models import Tag


class TagSerializerTests(APITestCase):
    """Класс тестов сериализатора для тэгов."""
    def setUp(self):
        self.tag_data = {
            'name': 'завтрак',
            'color': '#E26C2D',
            'slug': 'breakfast'
        }
        self.tag = Tag.objects.create(**self.tag_data)
        self.tag_url = 'http://testserver/api/tags/'

    def test_tag_list_data(self):
        """
        Тестируем данные,
        которые получаем при отображении всех тэгов.
        Доступно не авторизированному пользователю.
        """
        response = self.client.get(path=self.tag_url)
        tag_field_list = [
            {
                'id': self.tag.id,
                'name': self.tag.name,
                'color': self.tag.color,
                'slug': self.tag.slug
            }
        ]
        self.assertEqual(tag_field_list, response.json())

    def test_tag_by_id(self):
        """
        Тестируем данные,
        которые получаем при отображении тэга по id.
        Доступно не авторизированному пользователю.
        """
        tag_id_url = self.tag_url + str(self.tag.id) + '/'
        response = self.client.get(path=tag_id_url)
        data = response.json()
        tag_fields = (

            (self.tag.id, data.get('id')),
            (self.tag.name, data.get('name')),
            (self.tag.color, data.get('color')),
            (self.tag.slug, data.get('slug'))
        )
        for value, expected in tag_fields:
            with self.subTest(value=value):
                self.assertEqual(value, expected)
