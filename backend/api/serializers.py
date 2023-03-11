from django.db import transaction
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Subscription, Tag, TagRecipe)
from rest_framework import serializers
from users.models import User


class CustomUserSerializer(UserSerializer):

    is_subscribed = serializers.SerializerMethodField('check_if_is_subscribed')

    def check_if_is_subscribed(self, obj):
        current_user = self.context.get('current_user')
        if not current_user:
            return False
        return Subscription.objects.filter(
            subscriber=obj, author=current_user
        ).exists()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )


class TagSerializer(serializers.ModelSerializer):

    color = serializers.CharField(source='hex_code')

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientAmountSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class ReadRecipeSerializer(serializers.ModelSerializer):

    text = serializers.CharField(source='description')
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = IngredientAmountSerializer(source='ingredientrec', many=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)
    is_favorited = serializers.BooleanField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart'
        )


class WriteIngredientAmountSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(source='ingredient')

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')


class WriteRecipeSerializer(serializers.ModelSerializer):

    text = serializers.CharField(source='description')
    ingredients = WriteIngredientAmountSerializer(
        source='ingredientrec', many=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    image = Base64ImageField()
    is_in_shopping_cart = serializers.BooleanField(read_only=True)
    is_favorited = serializers.BooleanField(read_only=True)

    @transaction.atomic
    def create(self, validated_data):
        try:
            ingredients = validated_data.pop('ingredientrec')
        except KeyError:
            raise serializers.ValidationError(
                {'errors': 'Ингредиенты отсутствуют в запросе.'}
            )
        try:
            tags = validated_data.pop('tags')
        except KeyError:
            raise serializers.ValidationError(
                {'errors': 'Теги отсутствуют в запросе.'}
            )
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        create_ingredients = [
            IngredientAmount(
                recipe=recipe,
                ingredient=Ingredient.objects.get(
                    id=ingredient.get('ingredient')
                ),
                amount=ingredient.get('amount')
            )
            for ingredient in ingredients
        ]
        IngredientAmount.objects.bulk_create(create_ingredients)
        return recipe

    def update(self, instance, validated_data):
        try:
            ingredients = validated_data.pop('ingredientrec')
        except KeyError:
            raise serializers.ValidationError(
                {'errors': 'Ингредиенты отсутствуют в запросе.'}
            )
        try:
            tags = validated_data.pop('tags')
        except KeyError:
            raise serializers.ValidationError(
                {'errors': 'Теги отсутствуют в запросе.'}
            )
        TagRecipe.objects.filter(recipe=instance).delete()
        IngredientAmount.objects.filter(recipe=instance).delete()
        create_ingredients = [
            IngredientAmount(
                recipe=instance,
                ingredient=Ingredient.objects.get(
                    id=ingredient.get('ingredient')
                ),
                amount=ingredient.get('amount')
            )
            for ingredient in ingredients
        ]
        IngredientAmount.objects.bulk_create(create_ingredients)
        instance.name = validated_data.pop('name')
        instance.description = validated_data.pop('description')
        instance.cooking_time = validated_data.pop('cooking_time')
        try:
            instance.image = validated_data.pop('image')
        except KeyError:
            instance.image = instance.image
        instance.tags.set(tags)
        instance.save()
        return instance

    def to_representation(self, instance):
        user_id = self.context['request'].user.id
        instance = (Recipe.objects.add_user_annotations(user_id=user_id)
                    .get(id=instance.id))
        return ReadRecipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }).data

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'is_in_shopping_cart',
            'is_favorited',
            'cooking_time'
        )
        read_only_fields = ('author',)


class SubscriptionSerializer(serializers.ModelSerializer):

    subscriber = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    def validate(self, data):
        subscriber = data.get('subscriber')
        author = data.get('author')
        follow = Subscription.objects.filter(
            subscriber=subscriber, author=author
        )
        if follow.exists() and self.context.method == 'POST':
            raise serializers.ValidationError({'errors': 'Вы уже подписаны'})
        if not follow.exists() and self.context.method == 'DELETE':
            raise serializers.ValidationError(
                {'errors': 'Вы не были подписаны'}
            )
        if subscriber == author:
            raise serializers.ValidationError('На себя подписаться нельзя')
        return data

    class Meta:
        model = Subscription
        fields = ('subscriber', 'author')


class SpecialRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
        read_only_fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class ShowFollowerSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField('check_if_is_subscribed')
    recipes_count = serializers.SerializerMethodField('get_recipes_count')
    recipes = serializers.SerializerMethodField('get_recipes')

    def get_recipes(self, obj):
        recipes_limit_default = 6
        recipes_limit = None
        try:
            recipes_limit = int(self.context.get('recipes_limit'))
        except TypeError:
            recipes_limit = recipes_limit_default
        except ValueError:
            recipes_limit = recipes_limit_default
        if not recipes_limit:
            recipes = obj.recipe_author.all()
        else:
            recipes = obj.recipe_author.all()[:recipes_limit]
        return SpecialRecipeSerializer(recipes, many=True, read_only=True).data

    def check_if_is_subscribed(self, obj):
        current_user = self.context.get('current_user')
        if current_user is None:
            return False
        return Subscription.objects.filter(
            subscriber=obj, author=current_user
        ).exists()

    def get_recipes_count(self, obj):
        return obj.recipe_author.count()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )


class FavoriteSerializer(serializers.ModelSerializer):

    def to_representation(self, obj):
        recipe = Recipe.objects.get(id=obj.recipe.id)
        return SpecialRecipeSerializer(recipe, context=self.context).data

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')


class ShoppingCartSerializer(serializers.ModelSerializer):

    def validate(self, data):
        recipe = data.get('recipe')
        user = data.get('user')
        shopping_cart = ShoppingCart.objects.filter(user=user, recipe=recipe)
        if shopping_cart.exists() and self.context.method == 'POST':
            raise serializers.ValidationError(
                {'errors': 'Вы уже добавили рецепт в список покупок'}
            )
        if not shopping_cart.exists() and self.context.method == 'DELETE':
            raise serializers.ValidationError(
                {'errors': 'Рецепт не был добавлен в список покупок'}
            )
        return data

    def to_representation(self, obj):
        recipe = Recipe.objects.get(id=obj.recipe.id)
        return SpecialRecipeSerializer(recipe, many=False, read_only=True).data

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='recipe.id',
        read_only=True,
    )
    name = serializers.ReadOnlyField(
        source='recipe.name',
        read_only=True,
    )
    image = Base64ImageField(read_only=True, source='recipe.image',)
    cooking_time = serializers.ReadOnlyField(
        source='recipe.cooking_time',
        read_only=True,
    )

    def validate(self, data):
        user = self.context.get('request').user
        recipe = self.context.get('recipe_id')
        if Favorite.objects.filter(user=user,
                                   recipe=recipe).exists():
            raise serializers.ValidationError({
                'errors': 'Рецепт уже в избранном'})
        return data

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time')
