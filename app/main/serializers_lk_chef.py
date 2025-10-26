from rest_framework import serializers
from main.models import RecipeCategory

from main.helpers_serializers import validate_unexpected_fields, is_valid_email, serializer_logger


class LkChefCategoriesRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeCategory
        fields = [
            'id',
            'title',
            'created',
            'updated'
        ]

class LkChefAddRecipeInputSerializer(serializers.Serializer):
    title = serializers.CharField(
        label='title', 
        write_only=True, 
        required=True,
        allow_blank=False,
        max_length=250
    )
    html_description = serializers.CharField(
        label='html_description', 
        write_only=True, 
        required=True,
        allow_blank=False,
        max_length=40000
    )
    ingredients = serializers.CharField(
        label='ingredients', 
        write_only=True, 
        required=True,
        allow_blank=False,
        max_length=40000
    )
    steps = serializers.CharField(
        label='steps', 
        write_only=True, 
        required=True,
        allow_blank=False,
        max_length=40000
    )
    time_cooking = serializers.TimeField(
        label='time_cooking', 
        write_only=True, 
        required=True
    )
    id_category_recipe = serializers.IntegerField(
        required=True,
        write_only=True
    )
    @validate_unexpected_fields()
    def validate(self, attrs):
        return attrs


class LkChefUpdateRecipeInputSerializer(LkChefAddRecipeInputSerializer):
    id = serializers.IntegerField(
        required=True,
        write_only=True
    )
    @validate_unexpected_fields()
    def validate(self, attrs):
        return attrs
