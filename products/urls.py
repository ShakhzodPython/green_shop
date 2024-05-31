from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'products_reactions', ProductReactionAPIView)
router.register(r'carts', CartViewSetAPIView)
router.register(r'carts/items', CartItemViewSetAPIView)

urlpatterns = [
    path('categories/', ProductCategoryAPIView.as_view(), name='categories'),
    path('sizes/', ProductSizeAPIView.as_view(), name='sizes'),
    # Этот эндпоит выглядит так products/
    path('', ProductAPIView.as_view(), name='product'),
    # А этот так например products/1
    path('<int:pk>/', ProductDetailAPIView.as_view(), name='product_detail'),
    path('', include(router.urls)),

]
