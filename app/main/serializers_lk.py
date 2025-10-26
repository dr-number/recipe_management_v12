from rest_framework import serializers
from main.models import Recipe
from main.const import (
    RATING_RECIPE_CHOICES
)
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