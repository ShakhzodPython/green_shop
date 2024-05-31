from django.contrib import admin

from .models import *


# Register your models here.
@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'created_at']
    list_filter = ['created_at']


