from django.contrib import admin

from .models import *


# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_staff']
    search_fields = ('username', 'first_name', 'last_name', 'email')
