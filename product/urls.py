
from django.urls import path
from .views import CheckoutSessionView, CheckoutTemplateView, SuccessView, CancelView

app_name = 'product'

urlpatterns = [
    path('', CheckoutTemplateView.as_view(), name='index'),
    path('checkout/<pk>/', CheckoutSessionView.as_view(), name='checkout'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
]
