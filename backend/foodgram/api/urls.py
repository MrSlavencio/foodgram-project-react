from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewSet, FavoriteRecipeViewSet,
                    IngredientViewSet, RecipeViewSet, TagViewSet)

router = DefaultRouter()

router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)
router.register('users', CustomUserViewSet)
router.register(
    r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteRecipeViewSet,
    basename='favorite')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
