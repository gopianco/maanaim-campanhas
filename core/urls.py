from django.urls import path

from core.views import IndexView, mentioned


urlpatterns = [
    path('', IndexView.as_view(), name = 'index'),
    # path('process_payment', process_payment, name='payment'),
    path('mentioned', mentioned, name='mentioned'),
    path('mentioned/*', mentioned, name='mentioned')
]
