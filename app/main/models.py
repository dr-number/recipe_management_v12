import random
from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg, Count

from tinymce.models import HTMLField

from main.const import (
    KEY_USER_TYPES_CHOICES, KEY_USER_TYPE_CHEF, RATING_RECIPE_CHOICES
)
_FORMAT_TIME_CODE = '%Y-%m-%d %H:%M:%S'

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated')

    class Meta:
        abstract = True


class User(AbstractUser):
    type = models.CharField(
        max_length=35,
        choices=KEY_USER_TYPES_CHOICES,
        verbose_name='Роль',
        null=False,
        blank=False
    )
    favorites = models.ManyToManyField(
        to='Recipe',
        verbose_name='Избранное',
        blank=True,
        null=True,
        related_name='favorited_by'
    )
    is_confirmed_email = models.BooleanField(default=False, verbose_name='Подтвердение email')
    date_confirmed_email = models.DateTimeField(blank=True, null=True, verbose_name='Дата подтвердения email')
    confirmation_email = models.JSONField(verbose_name='код-подтвердение email', blank=True, default=dict)

    def new_confirmation_code_email(self) -> str:
        code = f'{random.randrange(1, 10 ** 4):04}'
        now = datetime.now()
        self.confirmation_email = {
            'code': code,
            'code_created': now.strftime(_FORMAT_TIME_CODE),
            'code_expiry': (now + timedelta(hours=1)).strftime(_FORMAT_TIME_CODE)
        }
        self.save(update_fields=['confirmation_email'])
        return code

    def check_confirmation_code(self, check_code: str) -> bool:
        data = self.confirmation_email
        code = data.get('code', None)
    
        _is_expired = False
        if data['code_expiry']:
            code_expiry = datetime.strptime(data['code_expiry'], _FORMAT_TIME_CODE)
            _is_expired = datetime.now() > code_expiry
            
        if not code:
            return None

        if _is_expired:
            turn_off_confirmation_code(self=self, type_data=type_data)

        data = getattr(self, f'confirmation_{type_data}', {})
        code = data.get('code', None)

        if not code:
            telegram_bot_send_msg(
                text=(
                    f'🛑 Код активации истек ({type_data}) check_confirmation_code (2)!\n'
                    f'{more_info}\n{_sub_info_data}'
                    f'Введенный код: <b>{check_code}</b>, Ожидаемый код: <b>{code}</b>\n'
                    f'Время жизни кода:\n{_time_info}'
                    '\n#error_check_confirmation_code'
                ),
                html=True,
                chat_id=ERRORS_CHAT_ID
            )
            return None

        if code == check_code:
            setattr(self, f'date_last_confirmed_{type_data}', datetime.now())
            turn_off_confirmation_code(self=self, type_data=type_data)
            return True
        else:
            telegram_bot_send_msg(
                text=(
                    f'🛑 Введен неверный код ({type_data}) ативации check_confirmation_code!\n'
                    f'{more_info}\n{_sub_info_data}'
                    f'Введенный код: <b>{check_code}</b>, Ожидаемый код: <b>{code}</b>\n'
                    f'Время жизни кода:\n{_time_info}'
                    '\n#error_check_confirmation_code'
                ),
                html=True,
                chat_id=ERRORS_CHAT_ID
            )
            return False

class RecipeCategory(BaseModel):
    title = models.CharField(null=False, blank=False, max_length=70, verbose_name='Название')

    def __str__(self) -> str:
        return self.title

class Recipe(BaseModel):
    title = models.CharField(null=False, blank=False, max_length=70, verbose_name='Название')
    html_description = HTMLField(verbose_name='Описание')
    ingredients = models.TextField(null=False, blank=False, verbose_name='ингредиенты')
    steps = models.TextField(null=False, blank=False, verbose_name='Шаги')
    time_cooking = models.TimeField(null=False, blank=False, verbose_name='время приготовления')
    type = models.ForeignKey(
        to=RecipeCategory,
        on_delete=models.PROTECT, 
        blank=True, 
        null=True, 
        verbose_name='Категория'
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT, 
        blank=False, 
        null=False, 
        verbose_name='Пользователь',
        help_text='Добавить рецепт может только шеф-повар',
        limit_choices_to={'type': KEY_USER_TYPE_CHEF}
    )
    class Meta: 
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self) -> str:
        return self.title

    @property
    def average_rating(self):
        result = self.comments.aggregate(average=Avg('raiting'))
        return result['average'] or 0
    
    @property
    def rating_count(self):
        return self.comments.count()
    
    @property
    def rating_distribution(self):
        """Распределение оценок"""
        return self.comments.values('raiting').annotate(count=Count('id')).order_by('raiting')
    
class Comment(BaseModel):
    text = models.TextField(null=False, blank=False, max_length=250, verbose_name='Комментарий')
    raiting = models.IntegerField(
        verbose_name='Рейтинг',
        choices=RATING_RECIPE_CHOICES,
        null=False,
        blank=False
    )
    recipe = models.OneToOneField(
        to=Recipe,
        on_delete=models.PROTECT, 
        blank=False, 
        null=False, 
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT, 
        blank=False, 
        null=False, 
        verbose_name='Пользователь'
    )
