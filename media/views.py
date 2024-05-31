from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Media
from .serializers import MediaSerializer


# Create your views here.


# ModelViewSet -> позволяет вам делать GET, PUT запросы и, так же перейти к объекту по id и изменять(PUT) его и удалять(DELETE)
class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = (IsAdminUser,)

    # perform_create -> Это метод, который используется для настройки или добавления дополнительной логики перед тем, как данные будут сохранены
    def perform_create(self, serializer):
        serializer.save()
