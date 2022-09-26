import csv

from django.db.models import Sum
from django.http.response import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.serializers import RecipeForUserSerializer

from .filters import IngredientFilter, RecipeFilter
from .models import Ingredient, IngredientRecipe, Recipe, Tag
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

    @action(
        methods=['get'],
        detail=False,
    )
    def download_shopping_cart(self, request):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        ingredients = IngredientRecipe.objects.filter(
            recipe_shopping_cart_user=request.user
        ).values(
            'ingredient_name', 'ingredient_measurement_unit'
        ).annotate(ingredient_amount=Sum('amount')).values_list(
            'ingredient_name', 'ingredient_measurement_unit',
            'ingredient_amount')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = ('attachment;'
                                           'filename="Shoppingcart.csv"')
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response)
        for item in list(ingredients):
            writer.writerow(item)
        return response
