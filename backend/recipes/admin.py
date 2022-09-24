from django.contrib import admin

from .models import Ingredient, IngredientRecipe, Recipe, Tag

EMPTY = '-пусто-'


class IngredientInline(admin.TabularInline):
    model = IngredientRecipe


@admin.register(IngredientRecipe)
class IngredientRecipe(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
    empty_value_display = EMPTY
    search_fields = ('ingredient__name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'image', 'cooking_time', 'author', 'get_ingredients',
        'get_tags', 'favorites_count', 'shopping_cart_count'
    )
    inlines = (IngredientInline,)
    empty_value_display = EMPTY
    list_filter = ('author', 'tags')
    search_fields = (
        'name', 'author__username', 'tags__name', 'ingredients__name'
    )

    def get_ingredients(self, obj):
        return Recipe.obj.ingridients.value_list('name')

    def get_tags(self, obj):
        return Recipe.tags.value_list('name')

    def favorites_count(self, obj):
        return obj.favorites.count()

    def shopping_cart_count(self, obj):
        return obj.shopping_cart.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    empty_value_display = EMPTY
    search_fields = ('name', 'measurement_unit')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    empty_value_display = EMPTY
    search_fields = ('name', 'color', 'slug')
