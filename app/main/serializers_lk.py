from rest_framework import serializers
from main.models import User, Recipe, Comment
from main.const import (
    RATING_RECIPE_CHOICES
)
from main.helpers_serializers import validate_unexpected_fields, is_valid_email, serializer_logger

class LkAllUserOutputSerializer(serializers.ModelSerializer):
    type_text = serializers.SerializerMethodField()
    is_chef = serializers.SerializerMethodField()

    def get_type_text(self, obj: User) -> str:
        return obj.get_type_text()

    def get_is_chef(self, obj: User) -> bool:
        return obj.is_chef()

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'type_text',
            'is_chef',
            'date_joined'
        ]

class LkAllCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'text',
            'raiting',
            'recipe',
            'user',
            'created',
            'updated'
        ]

class LkAllRecipesSerializer(serializers.ModelSerializer):
    text_time_cooking = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    name_chef = serializers.SerializerMethodField()

    def get_text_time_cooking(self, obj: Recipe) -> str:
        return obj.text_time_cooking()

    def get_category(self, obj: Recipe) -> str:
        return obj.get_title_category()

    def get_name_chef(self, obj: Recipe) -> str:
        return obj.user.get_name()
    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'category',
            'user',
            'text_time_cooking',
            'name_chef',
            'created',
            'updated'
        ]

class LkRecipeInputSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        required=True,
        write_only=True
    )
    @validate_unexpected_fields()
    def validate(self, attrs):
        return attrs

class LkRecipeAddCommentInputSerializer(serializers.Serializer):
    id_recipe = serializers.IntegerField(
        required=True,
        write_only=True
    )
    raiting = serializers.ChoiceField(
        label='raiting', 
        write_only=True, 
        allow_blank=False,
        required=True,
        choices=RATING_RECIPE_CHOICES
    )
    text = serializers.CharField(
        label='text', 
        write_only=True, 
        required=True,
        allow_blank=False,
        max_length=6000
    )
    @validate_unexpected_fields()
    def validate(self, attrs):
        return attrs

class LkRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'html_description',
            'ingredients',
            'steps',
            'time_cooking',
            'type',
            'user',
            'created',
            'updated'
        ]

class RecipeWithCommentsSerializer(serializers.Serializer):
    recipe = LkRecipeSerializer()
    comments = LkAllCommentsSerializer(many=True)
    comments_count = serializers.IntegerField()
    rating = serializers.FloatField()
    
    def to_representation(self, instance: Recipe):
        comments = instance.get_comments()
        comments_count = comments.count()
        return {
            'recipe': LkRecipeSerializer(instance).data,
            'comments_count': comments_count,
            'comments': LkAllCommentsSerializer(comments, many=True).data,
            'rating': instance.get_raiting()
        }
