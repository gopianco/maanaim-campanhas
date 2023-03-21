from django.urls import path

from core.views import IndexView, process_payment


urlpatterns = [
    path('', IndexView.as_view(), name = 'index'),
    path('process_payment', process_payment, name='payment'),
]
