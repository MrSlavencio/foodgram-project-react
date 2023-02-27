from rest_framework import viewsets 

from recipes.models import Tag, Ingredient, Reciepe, Subscription, Favorite, ShoppingCart
from .serializers import (
    TagSerializer, IngredientSerializer, ReadReciepeSerializer, 
    WriteReciepeSerializer, SubscriptionSerializer, ShowFollowerSerializer,
    FavoriteSerializer, ShoppingCartSerializer)
from djoser.views import UserViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from users.models import User
from djoser.conf import settings
from rest_framework.pagination import PageNumberPagination

from rest_framework import mixins
from django.shortcuts import get_object_or_404

class CustomUserViewSet(UserViewSet):
    pagination_class = LimitOffsetPagination
    
    
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

    @action(["post"], detail=False, url_path="set_{}".format(User.USERNAME_FIELD))
    def set_username(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(["post"], detail=False, url_path="reset_{}".format(User.USERNAME_FIELD))
    def reset_username(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(
        ["post"], detail=False, url_path="reset_{}_confirm".format(User.USERNAME_FIELD)
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
        follow = Subscription.objects.filter(subscriber=subscriber, author=author)
        data = {
            'subscriber': subscriber.id,
            'author': author.id,
        }
        if request.method == 'POST':
            if follow.exists():
                return Response(
                    {'errors': 'Вы уже подписаны'}, status=status.HTTP_400_BAD_REQUEST
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
        elif request.method == 'DELETE':
            if follow.exists():
                follow.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'errors': 'Пользователь не был подписан'}, status=status.HTTP_400_BAD_REQUEST)

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
        print(user_obj)
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
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    
    
class ReciepeViewSet(viewsets.ModelViewSet):
    # pagination_class = PageNumberPagination ################ поменять
    queryset = Reciepe.objects.all()
    serializer_class = ReadReciepeSerializer
    #serializer_class = WriteReciepeSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return WriteReciepeSerializer
        else:
            return ReadReciepeSerializer

    @action(methods=['delete', 'post'], detail=True)
    def favorite(self, request, pk=None):
        user = request.user
        reciepe = get_object_or_404(Reciepe, id=pk)
        favorite = Favorite.objects.filter(user=user, recipe=reciepe)
        data = {
            'recipe': pk,
            'user': user.pk
        }
        if request.method == 'POST':
            if favorite.exists():
                return Response(
                    {'errors': 'Вы уже добавили рецепт в избранное'}, status=status.HTTP_400_BAD_REQUEST
                )
            serializer = FavoriteSerializer(data=data, context=request)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'errors': 'Рецепт не был добавлен ранее в избранное'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    @action(methods=['delete', 'post'], detail=True)
    def shopping_cart(self, request, pk=None):
        user = request.user
        reciepe = get_object_or_404(Reciepe, id=pk)
        favorite = ShoppingCart.objects.filter(user=user, recipe=reciepe)
        data = {
            'recipe': pk,
            'user': user.pk
        }
        if request.method == 'POST':
            if favorite.exists():
                return Response(
                    {'errors': 'Вы уже добавили рецепт в список покупок'}, status=status.HTTP_400_BAD_REQUEST
                )
            serializer = ShoppingCartSerializer(data=data, context=request)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'errors': 'Рецепт не был добавлен в список покупок'}, status=status.HTTP_400_BAD_REQUEST)
