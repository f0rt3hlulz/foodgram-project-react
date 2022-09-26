from django.http.response import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from users.serializers import RecipeForUserSerializer

from .filters import IngredientFilter, RecipeFilter
from .models import (Ingredient, Recipe, Tag)
from .permissions import AuthPostAuthorChangesOrReadOnly
from .serializers import (IngredientSerializer, RecipeReadSerializer,
                          RecipeWriteSerializer, TagSerializer)
from .services import add_or_del_obj


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('^name',)
    filterset_class = IngredientFilter
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthPostAuthorChangesOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=["post", "delete"], detail=True)
    def favorite(self, request, pk):
        return add_or_del_obj(
            pk, request, request.user.favorites,
            RecipeForUserSerializer
        )

    @action(methods=["post", "delete"], detail=True)
    def shopping_cart(self, request, pk):
        return add_or_del_obj(
            pk, request, request.user.shopping_cart,
            RecipeForUserSerializer
        )

    @action(detail=False)
    def download_shopping_cart(self, request):
        shopping_cart = request.user.purchases.all()
        purchase_list = {}
        for purchase in shopping_cart:
            ingredients = purchase.recipe.ingredientrecipe_set.all()
            for ingredient in ingredients:
                name = ingredient.ingredient.name
                amount = ingredient.amount
                unit = ingredient.ingredient.measurement_unit
                if name not in purchase_list:
                    purchase_list[name] = {
                        'amount': amount,
                        'unit': unit
                    }
                else:
                    purchase_list[name]['amount'] = (purchase_list[name]
                                                     ['amount'] + amount)
        wishlist = []
        for item in purchase_list:
            wishlist.append(f'{item} ({purchase_list[item]["unit"]}) — '
                            f'{purchase_list[item]["amount"]} \n')
        wishlist.append('')
        wishlist.append('Приятных покупок!')
        response = HttpResponse(wishlist, 'Content-Type: application/pdf')
        response['Content-Disposition'] = 'attachment; filename="wishlist.pdf"'
        return response
