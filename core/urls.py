from django.urls import path

from core.views import IndexView, mentioned, verify_token


urlpatterns = [
    path('', IndexView.as_view(), name = 'index'),
    path('verify-token', verify_token, name = 'verify_token'),
    # path('process_payment', process_payment, name='payment'),
    path('mentioned', mentioned, name='mentioned'),
    path('mentioned/*', mentioned, name='mentioned')
]
