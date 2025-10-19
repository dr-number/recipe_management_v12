from django.db import models
from django.contrib.auth.models import AbstractUser
from main.const import KEY_USER_TYPES_CHOICES

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

