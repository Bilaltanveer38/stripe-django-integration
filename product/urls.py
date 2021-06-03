
from django.urls import path
from .views import CheckoutSessionView, CheckoutTemplateView, SuccessView, CancelView, stripe_webhook_view, \
    StripeIntentView


app_name = 'product'

urlpatterns = [
    path('', CheckoutTemplateView.as_view(), name='index'),
    path('webhook/stripe/', stripe_webhook_view, name='stripe-webhook'),
    path('create-intent/<pk>/', StripeIntentView.as_view(), name='stripe-intent'),
    path('checkout/<pk>/', CheckoutSessionView.as_view(), name='checkout'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
]
