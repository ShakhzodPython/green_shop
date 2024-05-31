from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import MediaViewSet

# Регистрация только ViewSet!
router = DefaultRouter()
router.register(r'', MediaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
