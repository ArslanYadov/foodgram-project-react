from rest_framework import status
from rest_framework.test import APITestCase
from recipes.models import Ingredient, Tag


class TagUrlTests(APITestCase):
    """Класс тестов URL адресов для тэга."""
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


class IngredientUrlTests(APITestCase):
    """Класс тестов URL адресов для ингредиентов."""
    def setUp(self):
        self.ingredient_url = 'http://testserver/api/ingredients/'

    def test_ingredient_url(self):
        """Тест доступности URL с ингредиентами."""
        response = self.client.get(path=self.ingredient_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_exists_ingredient_id_url(self):
        """
        Тестируем ответ URL по ингредиентам,
        если они ещё не созданны.
        """
        ingredient_id_url = self.ingredient_url + '1/'
        response = self.client.get(path=ingredient_id_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_exists_ingredient_id_url(self):
        """Тестируем ответ URL по существующему id ингредиента."""
        ingredient_data = {
            'name': 'Капуста',
            'measurement_unit': 'кг'
        }
        ingredient_data = Ingredient.objects.create(**ingredient_data)

        ingredient_id_url = self.ingredient_url + str(ingredient_data.id) + '/'
        response = self.client.get(path=ingredient_id_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
