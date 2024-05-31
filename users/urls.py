from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import UserRegistrationAPIView, LoginAPIView, LogoutAPIView, UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet)

# если у вас не ViewSet, пожалуйста регистрируй как обычно
urlpatterns = [
    path('sign_up/', UserRegistrationAPIView.as_view(), name='sign_up'),
    path('sign_in/', LoginAPIView.as_view(), name='sign_in'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('', include(router.urls)),
]