from django.test import TestCase

# tests.py
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from main.models import User, RecipeCategory, Recipe

from main.const import KEY_USER_TYPE_CHEF, KEY_USER_TYPE_CULINARY_ENTHUSIAST

class AddRecipeTestCase(TestCase):
    def setUp(self):
        """Настройка тестовых данных"""
        # Создаем тестовую категорию
        category_title = "Ужин"
        self.category, _ = RecipeCategory.objects.get_or_create(title=category_title)
        
        # Создаем валидного пользователя-повара
        self.valid_chef = User.objects.create_user(
            username='chef@example.com',
            email='chef@example.com',
            password='testpass123',
            first_name='Иван',
            last_name='Поваров',
            is_active=True,
            type=KEY_USER_TYPE_CHEF,
            is_confirmed_email=True,
            date_confirmed_email=timezone.now()
        )
        
        # Создаем невалидных пользователей для тестирования ограничений
        self.inactive_chef = User.objects.create_user(
            username='inactive_chef@example.com',
            email='inactive_chef@example.com',
            password='testpass123',
            is_active=False,  # Неактивный
            type=KEY_USER_TYPE_CHEF,
            is_confirmed_email=True,
            date_confirmed_email=timezone.now()
        )
        
        self.unconfirmed_chef = User.objects.create_user(
            username='unconfirmed@example.com',
            email='unconfirmed@example.com',
            password='testpass123',
            is_active=False,
            type=KEY_USER_TYPE_CHEF,
            is_confirmed_email=False,  # Email не подтвержден
            date_confirmed_email=None
        )
        
        self.regular_user = User.objects.create_user(
            username='regular@example.com',
            email='regular@example.com',
            password='testpass123',
            is_active=True,
            type=KEY_USER_TYPE_CULINARY_ENTHUSIAST,  # Не повар
            is_confirmed_email=True,
            date_confirmed_email=timezone.now()
        )
        
        # Создаем токены для всех пользователей
        self.valid_chef_token = Token.objects.create(user=self.valid_chef)
        self.inactive_chef_token = Token.objects.create(user=self.inactive_chef)
        self.unconfirmed_chef_token = Token.objects.create(user=self.unconfirmed_chef)
        self.regular_user_token = Token.objects.create(user=self.regular_user)
        
        # Данные для создания рецепта
        self.valid_recipe_data = {
            'title': 'Картофельное пюре',
            'ingredients': 'Грибы, мясо, картошка, лук',
            'steps': 'Берем и готовим',
            'id_category_recipe': self.category.id,
            'time_cooking': '00:30:00',
            'html_description': '<p>Описание рецепта</p>'
        }
        
        self.client = APIClient()
        self.url = 'http://localhost:8700/main/lk_chef/add_recipe/'

    def test_add_recipe_success(self):
        """Тест успешного добавления рецепта валидным поваром"""
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.valid_chef_token.key}')
        
        response = self.client.post(
            self.url,
            data=self.valid_recipe_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['recipe_id'], None)
        
        # Проверяем, что рецепт действительно создан в базе
        recipe = Recipe.objects.get(title=self.valid_recipe_data['title'])
        self.assertEqual(recipe.user, self.valid_chef)
        self.assertEqual(recipe.ingredients, 'Грибы, мясо, картошка, лук')

    def test_add_recipe_without_authentication(self):
        """Тест попытки добавления рецепта без авторизации"""
        response = self.client.post(
            self.url,
            data=self.valid_recipe_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 401)

    def test_add_recipe_with_invalid_token(self):
        """Тест попытки добавления рецепта с невалидным токеном"""
        self.client.credentials(HTTP_AUTHORIZATION='token invalid_token')
        
        response = self.client.post(
            self.url,
            data=self.valid_recipe_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 401)

    def test_add_recipe_by_inactive_chef(self):
        """Тест попытки добавления рецепта неактивным поваром"""
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.inactive_chef_token.key}')
        
        response = self.client.post(
            self.url,
            data=self.valid_recipe_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 401)

    def test_add_recipe_by_unconfirmed_chef(self):
        """Тест попытки добавления рецепта поваром с неподтвержденным email"""
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.unconfirmed_chef_token.key}')
        
        response = self.client.post(
            self.url,
            data=self.valid_recipe_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 401)

    def test_add_recipe_by_regular_user(self):
        """Тест попытки добавления рецепта обычным пользователем"""
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.regular_user_token.key}')
        
        response = self.client.post(
            self.url,
            data=self.valid_recipe_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 403)

    def test_add_recipe_with_missing_required_fields(self):
        """Тест добавления рецепта с отсутствующими обязательными полями"""
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.valid_chef_token.key}')
        
        invalid_data = {
            'title': 'Неполный рецепт',
            # Отсутствуют обязательные поля
        }
        
        response = self.client.post(
            self.url,
            data=invalid_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 400)

    def test_add_recipe_with_invalid_category(self):
        """Тест добавления рецепта с несуществующей категорией"""
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.valid_chef_token.key}')
        
        invalid_data = self.valid_recipe_data.copy()
        invalid_data['id_category_recipe'] = 999  # Несуществующий ID
        
        response = self.client.post(
            self.url,
            data=invalid_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['errorText'], "Категория не найдена!")

    def test_add_recipe_with_invalid_time_format(self):
        """Тест добавления рецепта с невалидным форматом времени"""
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.valid_chef_token.key}')
        
        invalid_data = self.valid_recipe_data.copy()
        invalid_data['time_cooking'] = 'invalid_time_format'
        
        response = self.client.post(
            self.url,
            data=invalid_data,
            format='json'
        )
        self.assertEqual(response.status_code, 400)

    def test_recipe_count_in_database(self):
        """Тест подсчета количества рецептов в базе данных"""
        initial_count = Recipe.objects.count()
        
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.valid_chef_token.key}')
        response = self.client.post(
            self.url,
            data=self.valid_recipe_data,
            format='json'
        )
        
        final_count = Recipe.objects.count()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(final_count, initial_count + 1)

    def test_recipe_author_assignment(self):
        """Тест правильного назначения автора рецепта"""
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.valid_chef_token.key}')
        
        response = self.client.post(
            self.url,
            data=self.valid_recipe_data,
            format='json'
        )
        
        recipe = Recipe.objects.get(title='Картофельное пюре')
        self.assertEqual(recipe.user, self.valid_chef)
        self.assertEqual(recipe.user.get_name(), 'Поваров Иван')

    def tearDown(self):
        """Очистка после тестов"""
        Recipe.objects.all().delete()
        User.objects.all().delete()
        RecipeCategory.objects.all().delete()
        Token.objects.all().delete()
