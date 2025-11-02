from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import User, Recipe, RecipeCategory, Comment
from main.filters import TimeCookingFilter, RatingFilter
from main.permissions import ChefUserRestrictedAdmin
@admin.register(User)
class UserAdmin(UserAdmin):
    def get_personal_info_fields(self, user: User):
        fields = User._meta.get_fields()
        excluded_fields = (
            'username', 'password', 'id'
        )
        personal_info_fields = [
            field.name for field in fields
            if field.name not in excluded_fields and not field.is_relation
        ]
        personal_info_fields.append('favorites')
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

    filter_horizontal = UserAdmin.filter_horizontal + ('favorites',)
    list_display = (
        'id',
        'email',
        'is_confirmed_email',
        'last_name',
        'first_name',
        'type',
        'is_active',
        'token'
    )

@admin.register(Recipe)
class RecipeAdmin(ChefUserRestrictedAdmin, admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'type',
        'time_cooking',
        'user',
        # 'show_raiting',
        'created',
        'updated'
    )
    search_fields = [
        'title'
    ]
    autocomplete_fields = [
        'user'
    ]
    list_filter = (
        'type',
        TimeCookingFilter,
        RatingFilter
    )
    readonly_fields = []
    def show_raiting(self, obj: Recipe):
        return obj.get_raiting()

    show_raiting.short_description = 'Рейтинг'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user' and not request.user.is_superuser:
            kwargs["queryset"] = User.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
  

@admin.register(RecipeCategory)
class RecipeCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'created',
        'updated'
    )

@admin.register(Comment)
class CommentAdmin(ChefUserRestrictedAdmin, admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'raiting',
        'recipe',
        'user',
        'created',
        'updated'
    )
    autocomplete_fields = [
        'user'
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
       
        return qs.filter(user=request.user, recipe__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'recipe' and not request.user.is_superuser:
            kwargs["queryset"] = Recipe.objects.filter(
                user__id=request.user.id
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
