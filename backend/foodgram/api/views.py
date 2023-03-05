from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Subscription, Tag)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from users.models import User

from .filters import IngredientFilter, RecipeFilter
from .mixins import CreateDestroyViewSet
from .permissions import IsAuthorOrReadOnly
from .serializers import (CustomUserSerializer, FavoriteRecipeSerializer,
                          IngredientSerializer, ReadRecipeSerializer,
                          ShoppingCartSerializer, ShowFollowerSerializer,
                          SubscriptionSerializer, TagSerializer,
                          WriteRecipeSerializer)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
    page_size_default = 6
    pagination_class.page_size = page_size_default
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CustomUserSerializer

    @action(["post"], detail=False)
    def activation(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(["post"], detail=False)
    def resend_activation(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(["post"], detail=False)
    def reset_password(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(["post"], detail=False)
    def reset_password_confirm(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(
        ["post"], detail=False, url_path="set_{}".format(User.USERNAME_FIELD)
    )
    def set_username(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(
        ["post"], detail=False, url_path="reset_{}".format(User.USERNAME_FIELD)
    )
    def reset_username(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(
        ["post"],
        detail=False,
        url_path="reset_{}_confirm".format(User.USERNAME_FIELD)
    )
    def reset_username_confirm(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(
        methods=['delete', 'post'],
        detail=True,
    )
    def subscribe(self, request, id=None):
        subscriber = request.user
        author = get_object_or_404(User, id=id)
        follow = Subscription.objects.filter(
            subscriber=subscriber, author=author
        )
        data = {
            'subscriber': subscriber.id,
            'author': author.id,
        }
        if request.method == 'POST':
            if follow.exists():
                return Response(
                    {'errors': 'Вы уже подписаны'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = SubscriptionSerializer(data=data, context=request)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer = ShowFollowerSerializer(
                author,
                context={
                    'current_user': subscriber,
                    'recipes_limit': request.query_params.get('recipes_limit')
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if follow.exists():
                follow.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'Пользователь не был подписан'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        methods=["get"],
        detail=False
    )
    def subscriptions(self, request):
        subscriber = request.user
        author = Subscription.objects.filter(subscriber=subscriber)
        user_obj = []
        for follow_obj in author:
            user_obj.append(follow_obj.author)
        paginator = PageNumberPagination()
        page_size_default = 6
        try:
            page_size = int(request.query_params.get('limit'))
        except TypeError:
            page_size = page_size_default
        except ValueError:
            page_size = page_size_default
        paginator.page_size = page_size
        result_page = paginator.paginate_queryset(user_obj, request)
        serializer = ShowFollowerSerializer(
            result_page,
            many=True,
            context={
                'current_user': subscriber,
                'recipes_limit': request.query_params.get('recipes_limit')
            }
        )
        return paginator.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):

    http_method_names = ['get']
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):

    http_method_names = ['get']
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [IngredientFilter]
    search_fields = ('^name',)
    permission_classes = (IsAuthenticatedOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):

    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = PageNumberPagination
    page_size_default = 6
    pagination_class.page_size = page_size_default
    queryset = Recipe.objects.all()
    serializer_class = ReadRecipeSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_queryset(self):
        return Recipe.objects.add_user_annotations(self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return WriteRecipeSerializer
        else:
            return ReadRecipeSerializer

    @action(methods=['delete', 'post'], detail=True)
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        shopping_cart = ShoppingCart.objects.filter(user=user, recipe=recipe)
        data = {
            'recipe': pk,
            'user': user.pk
        }
        if request.method == 'POST':
            if shopping_cart.exists():
                return Response(
                    {'errors': 'Вы уже добавили рецепт в список покупок'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = ShoppingCartSerializer(data=data, context=request)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if shopping_cart.exists():
                shopping_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'Рецепт не был добавлен в список покупок'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(methods=['get'], detail=False)
    def download_shopping_cart(self, request):
        recipes = (ShoppingCart.objects.filter(user=request.user)
                   .values('recipe_id'))
        ingredients = IngredientAmount.objects.filter(recipe__in=recipes)
        agr_shopping_cart = (
            ingredients.values(
                'ingredient__name', 'ingredient__measurement_unit'
            ).annotate(name=F('ingredient__name'),
                       unit=F('ingredient__measurement_unit'),
                       total=Sum('amount')).order_by('-total'))
        text = '\n'.join([
            f'{ingredient["name"]}: {ingredient["total"]} {ingredient["unit"]}'
            for ingredient in agr_shopping_cart
        ])
        filename = 'my_shopping_cart.txt'
        response = HttpResponse(text, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class FavoriteRecipeViewSet(CreateDestroyViewSet):

    serializer_class = FavoriteRecipeSerializer
    http_method_names = ['post', 'delete']

    def get_queryset(self):
        user = self.request.user.id
        return Favorite.objects.filter(user=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['recipe_id'] = self.kwargs.get('recipe_id')
        return context

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            recipe=get_object_or_404(
                Recipe,
                id=self.kwargs.get('recipe_id')
            )
        )

    @action(methods=('delete',), detail=True)
    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        favorite = Favorite.objects.filter(user=request.user, recipe=recipe)
        if favorite.exists():
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Рецепт не был добавлен ранее в избранное'},
            status=status.HTTP_400_BAD_REQUEST
        )
