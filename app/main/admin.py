from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import User, Recipe, RecipeCategory, Comment
from main.filters import TimeCookingFilter

@admin.register(User)
class UserAdmin(UserAdmin):
    def get_personal_info_fields(self, user: User):
        fields = User._meta.get_fields()
        excluded_fields = [
            'username', 'password', 'id'
        ]
        personal_info_fields = [
            field.name for field in fields
            if field.name not in excluded_fields and not field.is_relation
        ]
        return personal_info_fields

    def get_fieldsets(self, request, obj: User = None):
        fieldsets = super().get_fieldsets(request, obj)
        if not obj:
            return fieldsets

        fieldsets = (
            (None, {'fields': ('username', 'password')}),
            ('Personal info', {'fields': self.get_personal_info_fields(obj)}),
        )
        return fieldsets

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
    search_fields = [
        'title'
    ]
    autocomplete_fields = [
        'user'
    ]
    list_filter = [
        'type',
        # 'user',
        TimeCookingFilter
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
    autocomplete_fields = [
        'user'
    ]
