from django.db import models
from django.contrib.auth.models import AbstractUser

from tinymce.models import HTMLField

from main.const import KEY_USER_TYPES_CHOICES, KEY_USER_TYPE_CHEF

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

    def __str__(self) -> str:
        return self.title
    
class Comment(BaseModel):
    text = models.TextField(null=False, blank=False, max_length=250, verbose_name='Комментарий')
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
