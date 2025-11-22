from django.test import TestCase

# tests.py
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from main.models import User, RecipeCategory, Recipe, Comment

from main.const import KEY_USER_TYPE_CHEF, KEY_USER_TYPE_CULINARY_ENTHUSIAST
from app.settings import HOST

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
        self.url = f'{HOST}/main/lk_chef/add_recipe/'

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

    def test_add_recipe_with_extra_fields_fields(self):
        """Тест добавления рецепта с лишними полями"""
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.valid_chef_token.key}')
        
        invalid_data = self.valid_recipe_data.copy()
        invalid_data['extra_field'] = 'some_value'
        
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

class AddCommentTestCase(TestCase):
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
        self.inactive_user = User.objects.create_user(
            username='inactive_user@example.com',
            email='inactive_user@example.com',
            password='testpass123',
            is_active=False,  # Неактивный
            type=KEY_USER_TYPE_CULINARY_ENTHUSIAST,
            is_confirmed_email=True,
            date_confirmed_email=timezone.now()
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
        self.inactive_token = Token.objects.create(user=self.inactive_user)
        self.regular_user_token = Token.objects.create(user=self.regular_user)

        # Данные для создания рецепта
        self.recipe = Recipe.objects.create(
            title='Тестовый рецепт',
            user=self.valid_chef,
            ingredients='Тестовые ингредиенты',
            steps='Тестовые шаги',
            time_cooking='00:30:00',
            type=self.category
        )

        # Данные для создания комментария
        self.valid_comment_data = {
            'id_recipe': self.recipe.id,
            'raiting': 5,
            'text': 'Очень вкусно'
        }
        
        self.client = APIClient()
        self.url = self.url = f'{HOST}/main/lk_all/add_comment_to_recipe'

    def test_add_comment_success(self):
        """Тест успешного добавления комментария активным пользователем"""
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.regular_user_token.key}')
        
        response = self.client.post(
            self.url,
            data=self.valid_comment_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('comment_id', response.data)
        self.assertNotEqual(response.data['comment_id'], None)
        
        # Проверяем, что комментарий действительно создан в базе
        comment = Comment.objects.get(id=response.data['comment_id'])
        self.assertEqual(comment.user, self.regular_user_token)
        self.assertEqual(comment.recipe, self.recipe)
        self.assertEqual(comment.text, 'Очень вкусно')
        self.assertEqual(comment.raiting, 5)

    def test_add_comment_without_authentication(self):
        """Тест попытки добавления комментария без авторизации"""
        response = self.client.post(
            self.url,
            data=self.valid_comment_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 401)

    def test_add_comment_with_invalid_token(self):
        """Тест попытки добавления комментария с невалидным токеном"""
        self.client.credentials(HTTP_AUTHORIZATION='token invalid_token')
        
        response = self.client.post(
            self.url,
            data=self.valid_comment_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 401)

    def test_add_comment_by_inactive_user(self):
        """Тест попытки добавления комментария неактивным пользователем"""
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.inactive_token.key}')
        
        response = self.client.post(
            self.url,
            data=self.valid_comment_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 403)

    def test_add_comment_to_nonexistent_recipe(self):
        """Тест добавления комментария к несуществующему рецепту"""
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.regular_user_token.key}')
        
        invalid_data = self.valid_comment_data.copy()
        invalid_data['id_recipe'] = 999  # Несуществующий ID
        
        response = self.client.post(
            self.url,
            data=invalid_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertIn('errors', response.data)

    def test_add_comment_with_invalid_rating(self):
        """Тест добавления комментария с невалидным рейтингом"""
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.regular_user_token.key}')
        
        # Рейтинг меньше 1
        invalid_data = self.valid_comment_data.copy()
        invalid_data['raiting'] = 0
        
        response = self.client.post(
            self.url,
            data=invalid_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        
        # Рейтинг больше 5
        invalid_data['raiting'] = 6
        response = self.client.post(
            self.url,
            data=invalid_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])

    def test_add_comment_with_missing_required_fields(self):
        """Тест добавления комментария с отсутствующими обязательными полями"""
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.regular_user_token.key}')
        
        # Без текста
        invalid_data = {
            'id_recipe': self.recipe.id,
            'raiting': 5
            # Отсутствует text
        }
        
        response = self.client.post(
            self.url,
            data=invalid_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        
        # Без рейтинга
        invalid_data = {
            'id_recipe': self.recipe.id,
            'text': 'Комментарий без рейтинга'
            # Отсутствует raiting
        }
        
        response = self.client.post(
            self.url,
            data=invalid_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])

    def test_add_comment_with_empty_text(self):
        """Тест добавления комментария с пустым текстом"""
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.regular_user_token.key}')
        
        invalid_data = self.valid_comment_data.copy()
        invalid_data['text'] = ''  # Пустой текст
        
        response = self.client.post(
            self.url,
            data=invalid_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])

    def test_add_comment_with_too_long_text(self):
        """Тест добавления комментария с слишком длинным текстом"""
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.regular_user_token.key}')
        
        invalid_data = self.valid_comment_data.copy()
        invalid_data['text'] = 'а' * 251  # Превышает максимальную длину 250 символов
        
        response = self.client.post(
            self.url,
            data=invalid_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])

    def test_comment_count_in_database(self):
        """Тест подсчета количества комментариев в базе данных"""
        initial_count = Comment.objects.count()
        
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.regular_user_token.key}')
        response = self.client.post(
            self.url,
            data=self.valid_comment_data,
            format='json'
        )
        
        final_count = Comment.objects.count()
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(final_count, initial_count + 1)

    def test_comment_user_assignment(self):
        """Тест правильного назначения пользователя комментария"""
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.regular_user_token.key}')
        
        response = self.client.post(
            self.url,
            data=self.valid_comment_data,
            format='json'
        )
        
        comment = Comment.objects.get(id=response.data['comment_id'])
        self.assertEqual(comment.user, self.valid_user)
        self.assertEqual(comment.user.get_name(), 'Пользователь Тест')

    def test_multiple_comments_to_same_recipe(self):
        """Тест добавления нескольких комментариев к одному рецепту"""
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.regular_user_token.key}')
        
        # Первый комментарий
        response1 = self.client.post(
            self.url,
            data=self.valid_comment_data,
            format='json'
        )
        self.assertEqual(response1.status_code, 201)
        
        # Второй комментарий от того же пользователя
        second_comment_data = {
            'id_recipe': self.recipe.id,
            'raiting': 4,
            'text': 'Еще один комментарий'
        }
        
        response2 = self.client.post(
            self.url,
            data=second_comment_data,
            format='json'
        )
        
        self.assertEqual(response2.status_code, 201)
        
        # Проверяем, что оба комментария созданы
        comments_count = Comment.objects.filter(recipe=self.recipe).count()
        self.assertEqual(comments_count, 2)

    def test_comment_creation_timestamp(self):
        """Тест автоматического создания временных меток"""
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.regular_user_token.key}')
        
        response = self.client.post(
            self.url,
            data=self.valid_comment_data,
            format='json'
        )
        
        comment = Comment.objects.get(id=response.data['comment_id'])
        self.assertIsNotNone(comment.created_at)
        self.assertIsNotNone(comment.updated_at)
        self.assertLessEqual(comment.created_at, timezone.now())

    def tearDown(self):
        """Очистка после тестов"""
        Recipe.objects.all().delete()
        Comment.objects.all().delete()
        User.objects.all().delete()
        RecipeCategory.objects.all().delete()
        Token.objects.all().delete()
    