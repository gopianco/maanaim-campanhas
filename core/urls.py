from django.urls import path

from core.views import IndexView


urlpatterns = [
    path('', IndexView.as_view(), name = 'index'),
    path('updateItems/', IndexView.add_to_bag(), name='updateItems')
]
