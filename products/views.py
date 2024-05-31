from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Exists, OuterRef, Count

from rest_framework import generics, viewsets
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

from .serializers import (CategorySerializer,
                          SizeSerializer,
                          ProductsSerializer,
                          ProductDetailSerializer,
                          ProductsReactionsSerializer,
                          CartSerializer,
                          CartItemSerializer
                          )
from .models import *


# Create your views here.

class ProductCategoryAPIView(generics.ListAPIView):
    queryset = Category.objects.annotate(product_count=Count('products'))
    serializer_class = CategorySerializer


class ProductSizeAPIView(generics.ListAPIView):
    queryset = Size.objects.all().annotate(product_size=Count('products'))
    serializer_class = SizeSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]

    # get_queryset -> помогает выбрать нам какие объекты мы хотим получить объекты из БД
    def get_queryset(self):
        # кто является текущим пользователем веб-страницы
        user = self.request.user
        if user.is_authenticated:
            # Products.objects.annotate(...) -> это говорит Django, что вы хотите получить список всех продуктов, но также добавить дополнительную информацию к каждому продукту.
            return Products.objects.annotate(
                # Exists -> проверяет, есть ли запись в ProductsReactions, которая соответствует текущему пользователю и товару, и где is_liked=True
                # Если такая запись существует, is_liked будет True, в противном случае - False
                is_liked=Exists(
                    ProductsReactions.objects.filter(
                        user=user,
                        product=OuterRef('pk'),
                        # OuterRef('pk') -> в Django используется для ссылки на “внешний” объект в подзапросе. В данном случае, OuterRef('pk') ссылается на первичный ключ (pk) продукта в основном запросе.
                        is_liked=True
                    )
                ),
                # Avg -> это добавляет средний рейтинг каждого товара. Avg вычисляет среднее значение всех рейтингов в ProductsReactions для каждого товара
                rating=Avg('product_reaction__rating')
            )
        else:
            return Products.objects.all()


class ProductAPIView(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'price']
    ordering_fields = ['price', 'title']
    search_fields = ['title']

    def get_queryset(self):
        user = self.request.user
        # Проверяем, авторизован ли пользователь
        if user.is_authenticated:
            # annotate -> она добавляет дополнительные поля (is_liked и rating) к каждому продукту прямо при выполнении запроса, что делает процесс более быстрым и эффективным
            return Products.objects.annotate(
                is_liked=Exists(
                    ProductsReactions.objects.filter(
                        user=user,
                        product=OuterRef('pk'),
                        is_liked=True
                    )
                ),
            ).prefetch_related('looked')
        else:
            # если пользователь не авторизован, то возвращаем все продукты
            return Products.objects.all()


class ProductReactionAPIView(UpdateModelMixin, viewsets.GenericViewSet):
    queryset = ProductsReactions.objects.all()
    serializer_class = ProductsReactionsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'product'

    def get_object(self):
        obj, _ = ProductsReactions.objects.get_or_create(user=self.request.user,
                                                         product_id=self.kwargs['product'])
        return obj


class CartViewSetAPIView(CreateModelMixin, ListModelMixin, viewsets.GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.select_related('user').prefetch_related('cart_items')


class CartItemViewSetAPIView(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.select_related('cart', 'product')
