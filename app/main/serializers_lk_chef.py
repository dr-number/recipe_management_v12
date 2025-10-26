from rest_framework import serializers
from main.models import RecipeCategory


class LkAllRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeCategory
        fields = [
            'id',
            'title',
            'created',
            'updated'
        ]