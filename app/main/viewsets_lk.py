from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions, parsers, renderers
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth import logout

from main.serializers_lk import (
    LkAllRecipesSerializer, RecipeWithCommentsSerializer, LkRecipeInputSerializer, 
    LkRecipeAddCommentInputSerializer, LkAllCommentsSerializer, LkAllUserOutputSerializer,
    EditAccountSerializer
)
from main.forms import CommentForm
from main.models import Recipe, Comment, User
from main.const import CodesErrors
from main.helpers import get_recipe_params
from app.helpers import log_error_response


class LkAllViewSet(ViewSet):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes =(permissions.IsAuthenticated,)

    @swagger_auto_schema(request_body=EditAccountSerializer)
    @action(detail=False, methods=['post'])
    def edit_profile(self, request):
        serializer = EditAccountSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'code': CodesErrors.UNKNOWN_VALIDATION_ERROR, **serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        user: User = request.user
        user.first_name = serializer.validated_data.get('first_name', user.first_name)
        user.last_name = serializer.validated_data.get('last_name', user.last_name)
        user.type = serializer.validated_data.get('type', user.type)
        user.save(update_fields=['first_name', 'last_name', 'type'])

        return Response('ok')

    @swagger_auto_schema()
    @action(detail=False, methods=['get'])
    def list_all_recipes(self, request):
        return Response(
            LkAllRecipesSerializer(
                Recipe.objects.all().order_by('-created'), 
                many=True
            ).data
        )

    @swagger_auto_schema()
    @action(detail=False, methods=['get'])
    def get_user_info(self, request):
        return Response(
            LkAllUserOutputSerializer(
                request.user
            ).data
        )

    @action(detail=False, methods=['get'])
    def get_lk(self, request):
        return render(request, 'lk.html', {
            'user': LkAllUserOutputSerializer(request.user).data,
            
        })
    
    @action(detail=False, methods=['get'])
    def get_lk_list_all_recipes(self, request):
        list_all_recipes = Recipe.objects.all().order_by('-created')

        recipes = ''
        for item in list_all_recipes:
            recipes += render_to_string('includes/items/recipt.html', {
                'item': item,
                'category': item.get_title_category(),
                'raiting': item.get_raiting(),
                'name_chef': item.user.get_name(),
                'created': item.created.strftime('%d.%m.%Y'),
                'updated': item.updated.strftime('%d.%m.%Y')
            })
            
        return render(request, 'includes/list_all_recipes.html', {
            'user': request.user,
            'recipes': recipes
        })

    # @swagger_auto_schema(request_body=LkRecipeInputSerializer)
    @action(detail=False, methods=['get'])
    def get_recipe(self, request):
        query_params = request.query_params.dict()
        serializer = LkRecipeInputSerializer(data=query_params, context={'request': request})
        
        if not serializer.is_valid():
            return Response({'code': CodesErrors.UNKNOWN_VALIDATION_ERROR, **serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        recipe: Recipe = get_recipe_params(data={
            'id': serializer.validated_data['id']
        })

        if not recipe:
            return log_error_response(request, {
                'code': CodesErrors.NOT_FOUND,
                'errorText': (
                    'Данный рецепт не найден!'
                )
            })

        return Response(RecipeWithCommentsSerializer(recipe).data)

    @action(detail=False, methods=['get'])
    def get_lk_get_recipe(self, request):
        query_params = request.query_params.dict()
        serializer = LkRecipeInputSerializer(data=query_params, context={'request': request})
        
        if not serializer.is_valid():
            return Response({'code': CodesErrors.UNKNOWN_VALIDATION_ERROR, **serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        recipe: Recipe = get_recipe_params(data={
            'id': serializer.validated_data['id']
        })

        if not recipe:
            return log_error_response(request, {
                'code': CodesErrors.NOT_FOUND,
                'errorText': (
                    'Данный рецепт не найден!'
                )
            })

        comments: Comment = recipe.get_comments()
        comments_count = comments.count()

        list_comments = ''
        for item in comments:
            list_comments += render_to_string('includes/items/comment.html', {
                'item': item,
                'name_chef': item.user.get_name(),
                'created': item.created.strftime('%d.%m.%Y'),
                'updated': item.updated.strftime('%d.%m.%Y')
            })
            
        return render(request, 'get_recipe.html', {
            'user': request.user,
            'item': recipe,
            'rating': recipe.get_raiting(),
            'category': recipe.get_title_category(),
            'name_chef': recipe.user.get_name(),
            'created': recipe.created.strftime('%d.%m.%Y'),
            'updated': recipe.updated.strftime('%d.%m.%Y'),
            'comments_count': comments_count,
            'list_comments': list_comments,
            'comment_form': render_to_string('comment_form.html', {
                'form': CommentForm(initial={
                    'id_recipe': recipe.id
                })
            })
        })

    @swagger_auto_schema(request_body=LkRecipeAddCommentInputSerializer)
    @action(detail=False, methods=['post'])
    def add_comment_to_recipe(self, request):
        serializer = LkRecipeAddCommentInputSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'code': CodesErrors.UNKNOWN_VALIDATION_ERROR, **serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        recipe = get_recipe_params(data={
            'id': serializer.validated_data['id_recipe']
        })

        if not recipe:
            return log_error_response(request, {
                'code': CodesErrors.NOT_FOUND,
                'errorText': (
                    'Данный рецепт не найден!'
                )
            })

        new_comment = Comment.objects.create(
            recipe=recipe,
            raiting=serializer.validated_data['raiting'],
            text=serializer.validated_data['text'],
            user=request.user
        )

        return Response({
            'comment_id': new_comment.pk
        })

    @swagger_auto_schema()
    @action(detail=False, methods=['get'])
    def get_list_my_comments(self, request):
        return Response(
            LkAllCommentsSerializer(
                Comment.objects.filter(user=request.user).order_by('-created'), 
                many=True
            ).data
        )

    @swagger_auto_schema(request_body=LkRecipeInputSerializer)
    @action(detail=False, methods=['post'])
    def add_recipe_to_favorite(self, request):
        serializer = LkRecipeInputSerializer(data=request.data, context={'request': request})
        
        if not serializer.is_valid():
            return Response({'code': CodesErrors.UNKNOWN_VALIDATION_ERROR, **serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        recipe = get_recipe_params(data={
            'id': serializer.validated_data['id']
        })

        if not recipe:
            return log_error_response(request, {
                'code': CodesErrors.NOT_FOUND,
                'errorText': (
                    'Данный рецепт не найден!'
                )
            })

        user: User = request.user
        user.favorites.add(recipe)

        return Response('ok')

    @swagger_auto_schema()
    @action(detail=False, methods=['get'])
    def get_list_my_favorites(self, request):
        user: User = request.user
        return Response(
            LkAllRecipesSerializer(
                user.favorites.order_by('-created'), 
                many=True
            ).data
        )

    @action(detail=False, methods=['get'])
    def get_lk_list_my_favorites(self, request):
        user: User = request.user
        list_all_favorites = user.favorites.order_by('-created')

        favorites = ''
        for item in list_all_favorites:
            favorites += render_to_string('includes/items/recipt.html', {
                'item': item,
                'category': item.get_title_category(),
                'raiting': item.get_raiting(),
                'name_chef': item.user.get_name(),
                'created': item.created.strftime('%d.%m.%Y'),
                'updated': item.updated.strftime('%d.%m.%Y')
            })
            
        return render(request, 'includes/list_all_favorites.html', {
            'user': request.user,
            'recipes': favorites
        })

    @action(detail=False, methods=['get'])
    def get_lk_list_all_recipes_with_my_comments(self, request):
        user: User = request.user
        unique_recipes_with_my_comments = Recipe.objects.filter(
            comment__user=user
        ).distinct()

        favorites = ''
        for item in unique_recipes_with_my_comments:
            favorites += render_to_string('includes/items/recipt.html', {
                'item': item,
                'category': item.get_title_category(),
                'raiting': item.get_raiting(),
                'name_chef': item.user.get_name(),
                'created': item.created.strftime('%d.%m.%Y'),
                'updated': item.updated.strftime('%d.%m.%Y')
            })
            
        return render(request, 'includes/list_all_recipes_with_my_comments.html', {
            'user': request.user,
            'recipes': favorites
        })

    @swagger_auto_schema()
    @action(detail=False, methods=['post'])
    def logout(self, request):
        logout(request)
        return Response('ok')
