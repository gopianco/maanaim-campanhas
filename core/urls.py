from django.urls import path

from core.views import IndexView, SaleItemUpdateView


urlpatterns = [
    path('', IndexView.as_view(), name = 'index'),
    path('updateItem/', SaleItemUpdateView)
]
