from django.contrib import admin

from .models import Bread, Campaing

class AdminBread(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'slug', 'weight']
    search_fields = ['name', 'description', 'price', 'slug', 'weight']

class AdminCampaing(admin.ModelAdmin):
    list_display = ['delivery_date', 'slug', 'sales']
    search_fields = ['delivery_date', 'slug', 'sales']

admin.site.register(Bread, AdminBread)
admin.site.register(Campaing, AdminCampaing)