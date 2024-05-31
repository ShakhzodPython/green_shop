from django.contrib import admin

from .models import *


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count', 'created_at']
    list_filter = ['created_at']

    def product_count(self, obj):
        return Products.objects.filter(category=obj).count()


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_size', 'created_at']
    list_filter = ['created_at']

    def product_size(self, obj):
        return Products.objects.filter(size=obj).count()


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    list_filter = ['created_at']


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'size', 'quantity', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title']


@admin.register(ProductsReactions)
class UserProductRelationAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'is_liked', 'rating']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price', 'created_at']
    list_filter = ['created_at']

    def total_price(self, obj):
        return obj.get_total_price()

    total_price.short_description = 'Total Price'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']
