from django.contrib import admin
from .models import Ingredient, Tag, Recipe, IngredientAmount, TagRecipe


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit') 
    search_fields = ('name',) 
    list_filter = ('name',)
    
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_code', 'slug')
    
class IngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    
class TagsInLine(admin.TabularInline):
    model = Recipe.tags.through
    
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author') 
    list_filter = ('name', 'author', 'tags')
    inlines = [
        IngredientsInLine,
        TagsInLine
    ]


    


admin.site.register(Ingredient, IngredientAdmin)

admin.site.register(IngredientAmount)

admin.site.register(Tag, TagAdmin)

admin.site.register(TagRecipe)

admin.site.register(Recipe, RecipeAdmin)


# from django.contrib import admin
# from . import models

# admin.site.register(models.Tag)
# admin.site.register(models.Ingredient)


# class IngredientsInLine(admin.TabularInline):
#     model = models.Recipe.ingredients.through

# @admin.register(models.Recipe)
# class RecipeAdmin(admin.ModelAdmin):
#     inlines = [
#         IngredientsInLine,
#     ]
