from django.contrib import admin
from .models import Unit, Ingredient, Tag, Reciepe, IngredientAmount, TagReciepe


class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name') 
    search_fields = ('name',) 


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit') 
    search_fields = ('name',) 
    list_filter = ('name',)
    

class ReciepeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author') 
    list_filter = ('name', 'author', 'tags')

admin.site.register(Unit, UnitAdmin)

admin.site.register(Ingredient, IngredientAdmin)

admin.site.register(IngredientAmount)

admin.site.register(Tag)

admin.site.register(TagReciepe)

admin.site.register(Reciepe, ReciepeAdmin)
