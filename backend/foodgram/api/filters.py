import django_filters as filters
from recipes.models import Recipe, Tag
from rest_framework.filters import SearchFilter


class RecipeFilter(filters.FilterSet):

    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
    )
    is_favorited = filters.CharFilter(method='get_is_favorited')
    is_in_shopping_cart = filters.CharFilter(
        method='get_is_in_shopping_cart',
    )

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value == '1':
            return queryset.filter(favorite__user=user)
        if value == '0':
            return queryset.exclude(favorite__user=user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value == '1':
            return queryset.filter(in_shoppingcard__user=user)
        if value == '0':
            return queryset.exclude(in_shoppingcard__user=user)
        return queryset


class IngredientFilter(SearchFilter):

    search_param = 'name'
