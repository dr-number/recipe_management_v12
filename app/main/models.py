from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg, Count

from tinymce.models import HTMLField

from main.const import (
    KEY_USER_TYPES_CHOICES, KEY_USER_TYPE_CHEF, RATING_RECIPE_CHOICES
)

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
