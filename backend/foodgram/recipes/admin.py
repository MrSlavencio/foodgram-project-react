from django.contrib import admin
from .models import Unit, Ingredient, IngredientsInReciepe, Tag, Reciepe


class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name') 
    search_fields = ('name',) 


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit') 
    search_fields = ('name',) 
    list_filter = ('name',)
    
    
class IngredietsInReciepeAdmin(admin.ModelAdmin):
    list_display = ('ingredient',)
    search_fields = ('ingredient',)
    list_filter = ('ingredient',)

class ReciepeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author') 
    list_filter = ('name', 'author', 'tag')

admin.site.register(Unit, UnitAdmin)

admin.site.register(Ingredient, IngredientAdmin)

admin.site.register(IngredientsInReciepe, IngredietsInReciepeAdmin)

admin.site.register(Tag)

admin.site.register(Reciepe, ReciepeAdmin)
