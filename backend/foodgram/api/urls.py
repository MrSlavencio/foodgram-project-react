from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import TagViewSet, IngredientViewSet, CustomUserViewSet, ReciepeViewSet

router = DefaultRouter()

router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', ReciepeViewSet)
#router.register(r'^users/{pk}/subscribe$', SubscriptionViewSet)

router.register('users', CustomUserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken'))
]
