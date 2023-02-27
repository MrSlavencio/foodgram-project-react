from rest_framework import serializers
from django.db import transaction

from recipes.models import Tag, Ingredient, Reciepe, IngredientAmount, Subscription, TagReciepe, Favorite, ShoppingCart

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
    
    measurement_unit = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        
        
class IngredientAmountSerializer(serializers.ModelSerializer):
    
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit.short_name')
    #amount = serializers.CharField(source='quantity')
    
    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')
        
        
class ReadReciepeSerializer(serializers.ModelSerializer):
    
    text = serializers.CharField(source='description')
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = IngredientAmountSerializer(source='ingredientrec', many=True)
    
    class Meta:
        model = Reciepe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image', 'text', 'cooking_time')
        
        
class WriteIngredientAmountSerializer(serializers.ModelSerializer):
        
    id = serializers.IntegerField(source='ingredient')
    
    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')

        
class WriteReciepeSerializer(serializers.ModelSerializer):
    
    text = serializers.CharField(source='description')
    ingredients = WriteIngredientAmountSerializer(source='ingredientrec', many=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    
    class Meta:
        model = Reciepe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image', 'text', 'cooking_time')
        read_only_fields = ('author',)
    
    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredientrec')
        tags = validated_data.pop('tags')
        reciepe = Reciepe.objects.create(**validated_data)
        reciepe.tags.set(tags)
        create_ingredients = [
            IngredientAmount(
                reciepe=reciepe,
                ingredient=Ingredient.objects.get(id=ingredient['ingredient']),
                amount=ingredient['amount']
            )
            for ingredient in ingredients
        ]
        IngredientAmount.objects.bulk_create(create_ingredients)       
        return reciepe
    
    def update(self, instance, validated_data):
        print(validated_data)
        ingredients = validated_data.pop('ingredientrec')
        tags = validated_data.pop('tags')
        TagReciepe.objects.filter(reciepe=instance).delete()
        IngredientAmount.objects.filter(reciepe=instance).delete()
        create_ingredients = [
            IngredientAmount(
                reciepe=instance,
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
    
    def to_representation(self, obj):
        return ReadReciepeSerializer(obj, context=self.context).data



    
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
    class Meta:
        model = Reciepe
        fields = (
            'id',
            'name',
            #'image',
            'cooking_time'
        )


class ShowFollowerSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField('check_if_is_subscribed')
    reciepes_count = serializers.SerializerMethodField('get_reciepes_count')
    reciepes = serializers.SerializerMethodField('get_recipes')

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'reciepes',
            'reciepes_count'
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
            recipes = Reciepe.objects.filter(author=obj)
        else:
            recipes = Reciepe.objects.filter(author=obj)[:recipes_limit]
        return SpecialRecipeSerializer(recipes, many=True, read_only=True).data

    def check_if_is_subscribed(self, obj):
        current_user = self.context.get('current_user')
        if current_user is None:
            return False
        return Subscription.objects.filter(
            subscriber=obj, author=current_user
        ).exists()

    def get_reciepes_count(self, obj):
        count = Reciepe.objects.filter(author=obj).count()
        return count



class FavoriteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        
    def to_representation(self, obj):
        recipe = Reciepe.objects.get(id=obj.recipe.id)
        return SpecialRecipeSerializer(recipe, context=self.context).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')
        
    def to_representation(self, obj):
        recipe = Reciepe.objects.get(id=obj.recipe.id)
        return SpecialRecipeSerializer(recipe, context=self.context).data
