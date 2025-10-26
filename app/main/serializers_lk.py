from rest_framework import serializers
from main.models import Recipe, Comment
from main.const import (
    RATING_RECIPE_CHOICES
)
from main.helpers_serializers import validate_unexpected_fields, is_valid_email, serializer_logger

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
    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'type',
            'user',
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