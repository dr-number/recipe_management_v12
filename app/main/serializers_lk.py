from rest_framework import serializers
from main.models import Recipe

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