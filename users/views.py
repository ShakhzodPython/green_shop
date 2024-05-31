from django.contrib.auth import authenticate, logout
from django.utils.translation import gettext_lazy as _

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import status, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import viewsets

from .models import Profile
from .serializers import UserRegistrationSerializer, ProfileSerializer


# Create your views here.

# Регистрация пользователя
class UserRegistrationAPIView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    # Чтобы swagger показывал параметры
    @swagger_auto_schema(request_body=UserRegistrationSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'success': _(f'User {user.username} is created'),
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Авторизация пользователя
class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    # manual_parameters предназначен для ручного определения параметров в наш случаи это username и password
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
        }
    ))
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'success': _(f'User {user.username} is logged in'),
                'token': token.key
            }, status=status.HTTP_200_OK)
        return Response({
            'error': _('Username or password is incorrect')
        }, status=status.HTTP_400_BAD_REQUEST)


# Выход пользователя
class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description=_("Logout user from system"),
        responses={200: openapi.Response(description=_("Successfully logout from system"))}
    )
    def post(self, request):
        username = request.user.username if request.user else "Anonymous"
        # Выход пользователя из системы
        logout(request)
        return Response({"success": _(f"User {username} successfully logged out.")},
                        status=status.HTTP_200_OK)


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)



