from rest_framework import serializers
from django.db import transaction
from drf_extra_fields.fields import Base64ImageField

from recipes.models import Tag, Ingredient, Recipe, IngredientAmount, Subscription, TagRecipe, Favorite, ShoppingCart

from users.models import User

from djoser.serializers import UserSerializer
from rest_framework.validators import UniqueTogetherValidator


class CustomUserSerializer(UserSerializer):
    
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class TagSerializer(serializers.ModelSerializer):
    
    color = serializers.CharField(source='hex_code')

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    
    #measurement_unit = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        
        
class IngredientAmountSerializer(serializers.ModelSerializer):
    
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    #measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit.short_name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')
    #amount = serializers.CharField(source='quantity')
    
    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')
        
        
class ReadRecipeSerializer(serializers.ModelSerializer):
    
    text = serializers.CharField(source='description')
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = IngredientAmountSerializer(source='ingredientrec', many=True)
    is_in_shopping_cart = serializers.BooleanField()
    is_favorited = serializers.BooleanField()
    # is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()
    
    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image', 'text', 'cooking_time', 'is_favorited', 'is_in_shopping_cart')
        
    # def get_is_favorited(self, obj):
    #     return (self.context.get('request').user.is_authenticated
    #             and Favorite.objects.filter(
    #                 user=self.context.get('request').user,
    #                 recipe=obj
    #     ).exists())

    # def get_is_in_shopping_cart(self, obj):
    #     return (self.context.get('request').user.is_authenticated
    #             and ShoppingCart.objects.filter(
    #                 user=self.context.get('request').user,
    #                 recipe=obj
    #     ).exists())
        
        
class WriteIngredientAmountSerializer(serializers.ModelSerializer):
        
    id = serializers.IntegerField(source='ingredient')
    
    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')

        
class WriteRecipeSerializer(serializers.ModelSerializer):
    
    text = serializers.CharField(source='description')
    ingredients = WriteIngredientAmountSerializer(source='ingredientrec', many=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    image = Base64ImageField()
    
    is_in_shopping_cart = serializers.BooleanField(read_only=True)
    is_favorited = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image', 'text', 'is_in_shopping_cart', 'is_favorited', 'cooking_time')
        read_only_fields = ('author',)
    
    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredientrec')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        create_ingredients = [
            IngredientAmount(
                recipe=recipe,
                ingredient=Ingredient.objects.get(id=ingredient['ingredient']),
                amount=ingredient['amount']
            )
            for ingredient in ingredients
        ]
        IngredientAmount.objects.bulk_create(create_ingredients)       
        return recipe
    
    def update(self, instance, validated_data):
        # print(validated_data)
        ingredients = validated_data.pop('ingredientrec')
        tags = validated_data.pop('tags')
        TagRecipe.objects.filter(recipe=instance).delete()
        IngredientAmount.objects.filter(recipe=instance).delete()
        create_ingredients = [
            IngredientAmount(
                recipe=instance,
                ingredient=Ingredient.objects.get(id=ingredient['ingredient']),
                amount=ingredient['amount']
            )
            for ingredient in ingredients
        ]
        IngredientAmount.objects.bulk_create(create_ingredients)
        instance.name = validated_data.pop('name')
        instance.description = validated_data.pop('description')
        # if validated_data.get("image") is not None:
        #     instance.image = validated_data.pop("image")
        instance.cooking_time = validated_data.pop('cooking_time')
        instance.tags.set(tags)
        instance.save()
        return instance
    
    # def to_representation(self, obj):
    #     return ReadRecipeSerializer(obj, context=self.context).data
    
    def to_representation(self, instance):
        user_id = self.context['request'].user.id
        instance = Recipe.objects.add_user_annotations(user_id=user_id).get(id=instance.id)
        return ReadRecipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }).data



    
###    ок
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
        if subscriber == author:
            raise serializers.ValidationError('На себя подписаться нельзя')
        return data
    
    class Meta:
        model = Subscription
        fields = ('subscriber', 'author')
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=['subscriber', 'author'],
            )
        ]

###
class SpecialRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

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

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        ]
        
    def get_recipes(self, obj):
        recipes_limit = None
        try:
            recipes_limit = int(self.context.get('recipes_limit'))
        except TypeError:
            None
        except ValueError:
            None
        if not recipes_limit:
            recipes = Recipe.objects.filter(author=obj)
        else:
            recipes = Recipe.objects.filter(author=obj)[:recipes_limit]
        return SpecialRecipeSerializer(recipes, many=True, read_only=True).data

    def check_if_is_subscribed(self, obj):
        current_user = self.context.get('current_user')
        if current_user is None:
            return False
        return Subscription.objects.filter(
            subscriber=obj, author=current_user
        ).exists()

    def get_recipes_count(self, obj):
        count = Recipe.objects.filter(author=obj).count()
        return count



class FavoriteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        
    def to_representation(self, obj):
        recipe = Recipe.objects.get(id=obj.recipe.id)
        return SpecialRecipeSerializer(recipe, context=self.context).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')
        
    def to_representation(self, obj):
        recipe = Recipe.objects.get(id=obj.recipe.id)
        return SpecialRecipeSerializer(recipe, context=self.context).data






######

class FavoriteRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='recipe.id',
        read_only=True,
    )
    name = serializers.ReadOnlyField(
        source='recipe.name',
        read_only=True,
    )
    # image = serializers.CharField(
    #     source='recipe.image',
    #     read_only=True,
    # )
    image = Base64ImageField(read_only=True, source='recipe.image',)
    cooking_time = serializers.ReadOnlyField(
        source='recipe.cooking_time',
        read_only=True,
    )

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time')

    def validate(self, data):
        user = self.context.get('request').user
        recipe = self.context.get('recipe_id')
        if Favorite.objects.filter(user=user,
                                         recipe=recipe).exists():
            raise serializers.ValidationError({
                'errors': 'Рецепт уже в избранном'})
        return data
