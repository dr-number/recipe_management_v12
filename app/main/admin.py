from django.contrib import admin
from main.models import User, Recipe, RecipeCategory, Comment

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'last_name',
        'first_name',
        'type'
    ]

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'type',
        'time_cooking',
        'created',
        'updated'
    ]

@admin.register(RecipeCategory)
class RecipeCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'created',
        'updated'
    ]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'text',
        'recipe',
        'user',
        'created',
        'updated'
    ]
