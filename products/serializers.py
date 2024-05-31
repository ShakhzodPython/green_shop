from django.utils.translation import gettext_lazy as _

from .models import *
from users.models import Profile
from media.models import Media

from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'product_count')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ('id', 'file')


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'title')


class SizeSerializer(serializers.ModelSerializer):
    product_size = serializers.IntegerField()

    class Meta:
        model = Size
        fields = ('id', 'title', 'product_size')


class ProductsReactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsReactions
        fields = ('id', 'user', 'product', 'is_liked', 'rating')


class ProductLookedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'last_name')


class ProductsSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    is_liked = serializers.BooleanField(read_only=True)
    looked_users = ProductLookedSerializer(many=True, source='looked')

    class Meta:
        model = Products
        fields = ('id', 'title', 'price', 'images', 'is_liked', 'looked_users')


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    is_liked = serializers.BooleanField(read_only=True)
    rating = serializers.IntegerField(read_only=True)
    images = ProductImageSerializer(many=True)
    size = SizeSerializer(many=False)
    tags = TagsSerializer(many=True)

    class Meta:
        model = Products
        fields = ('title', 'rating', 'images', 'short_description', 'size',
                  'quantity', 'is_liked', 'sku', 'category', 'tags',
                  'description')


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'product', 'quantity')


class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()
    cart_items = CartItemSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), write_only=True, allow_null=True)
    owner = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'owner', 'total_price', 'cart_items')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'users', 'products', 'comment')
