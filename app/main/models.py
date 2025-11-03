import random
from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg
from django.dispatch import receiver

from django.db.models.signals import post_save

from tinymce.models import HTMLField
from rest_framework.authtoken.models import Token



from main.const import (
    KEY_USER_TYPES_CHOICES, KEY_USER_TYPE_CHEF, RATING_RECIPE_CHOICES, KEY_USER_TYPES_CHOICES_DICT
)
from app.settings import ERRORS_CHAT_ID

_FORMAT_TIME_CODE = '%Y-%m-%d %H:%M:%S'

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated')

    class Meta:
        abstract = True


class User(AbstractUser):
    is_active = models.BooleanField(default=False, verbose_name='Активная учетная запись')
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

    def get_type_text(self) -> str:
        return (
            'Администратор' if self.is_superuser else
            KEY_USER_TYPES_CHOICES_DICT.get(self.type, 'Неизвестно')
        )

    @property
    def token(self):
        """Get token."""
        return Token.objects.get_or_create(user=self)[0]

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

    def turn_off_confirmation_code(self):
        self.confirmation_email = {
            'code': None,
            'code_created': None,
            'code_expiry': None
        }
        self.save(update_fields=['confirmation_email'])

    def check_confirmation_code(self, check_code: str) -> bool:
        from main.helpers import telegram_bot_send_msg

        data = self.confirmation_email
        code = data.get('code', None)
        _time_info = ''
        _is_expired = False

        if data['code_expiry']:
            code_expiry = datetime.strptime(data['code_expiry'], _FORMAT_TIME_CODE)
            _is_expired = datetime.now() > code_expiry
            _time_info = (
                f"Просрочен: <b>{_is_expired}</b>\n"
                f"Now: <b>{datetime.now().strftime(_FORMAT_TIME_CODE)}</b>\n"
                f"code_expiry: <b>{code_expiry.strftime(_FORMAT_TIME_CODE)}</b>"
            )
            
        if not code:
            return None

        if _is_expired:
            self.turn_off_confirmation_code()

        data = self.confirmation_email
        code = data.get('code', None)

        if not code:
            telegram_bot_send_msg(
                text=(
                    f'🛑 Код активации истек check_confirmation_code (2)!\n'
                    f'Введенный код: <b>{check_code}</b>, Ожидаемый код: <b>{code}</b>\n'
                    f'Время жизни кода:\n{_time_info}'
                    '\n#error_check_confirmation_code'
                ),
                html=True,
                chat_id=ERRORS_CHAT_ID
            )
            return None

        if code == check_code:
            self.date_confirmed_email = datetime.now()
            self.save(update_fields=['date_confirmed_email'])
            self.turn_off_confirmation_code()
            return True
        else:
            telegram_bot_send_msg(
                text=(
                    f'🛑 Введен неверный код  check_confirmation_code!\n'
                    f'Введенный код: <b>{check_code}</b>, Ожидаемый код: <b>{code}</b>\n'
                    f'Время жизни кода:\n{_time_info}'
                    '\n#error_check_confirmation_code'
                ),
                html=True,
                chat_id=ERRORS_CHAT_ID
            )
            return False

@receiver(post_save, sender=User)
def save_user(sender, instance: User, created, **kwargs):
    from main.permissions import get_or_create_admin_shef

    if instance.is_superuser:
        return

    should_be_staff = instance.type == KEY_USER_TYPE_CHEF
    User.objects.filter(id=instance.id).update(is_staff=should_be_staff)

    if should_be_staff:
        instance.groups.add(get_or_create_admin_shef())
    else:
        instance.groups.remove(get_or_create_admin_shef())

class RecipeCategory(BaseModel):
    title = models.CharField(null=False, blank=False, max_length=70, verbose_name='Название')

    def __str__(self) -> str:
        return self.title

    class Meta: 
        verbose_name = "Категория рецепта"
        verbose_name_plural = "Категории рецептов"

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

    def text_time_cooking(self):
        hours = self.time_cooking.hour
        minutes = self.time_cooking.minute
        
        parts = []
        if hours > 0:
            parts.append(f"{hours} ч.")
        if minutes > 0:
            parts.append(f"{minutes} мин.")
        
        return ' '.join(parts) if parts else "0 мин."

    def get_comments(self):
        return Comment.objects.filter(recipe=self).order_by('-created')

    def get_raiting(self):
        average_rating = Comment.objects.filter(recipe=self).exclude(user=self.user).aggregate(
            avg_rating=Avg('raiting')
        )['avg_rating']
                               
        if average_rating is not None:
            return round(average_rating, 2)
        
        return 0
    
class Comment(BaseModel):
    text = models.TextField(null=False, blank=False, max_length=250, verbose_name='Комментарий')
    raiting = models.IntegerField(
        verbose_name='Рейтинг',
        choices=RATING_RECIPE_CHOICES,
        null=False,
        blank=False
    )
    recipe = models.ForeignKey(
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

    class Meta: 
        verbose_name = "Комментарий к рецепту"
        verbose_name_plural = "Комментарии к рецептам"

    
