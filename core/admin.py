from django.contrib import admin

from .models import Bread

class AdminBread(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'slug', 'weight']
    search_fields = ['name', 'description', 'price', 'slug', 'weight']

admin.site.register(Bread, AdminBread)