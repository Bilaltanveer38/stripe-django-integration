from django.conf import settings
from django.views import View
from .models import Product
from django.views.generic.base import TemplateView
import stripe
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.

class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelView(TemplateView):
    template_name = 'cancel.html'


class CheckoutTemplateView(TemplateView):
    template_name = 'landing_page.html'

    products = Product.objects.all().first()

    def get_context_data(self, **kwargs):
        context = super(CheckoutTemplateView, self).get_context_data(**kwargs)
        context.update({
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
            "product": self.products
        })
        return context


class CheckoutSessionView(View):

    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = 'http://127.0.0.1:8000/'
        pk = self.kwargs['pk']
        product = Product.objects.get(pk=pk)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': product.price,
                        'product_data': {
                            'name': product.name,
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + 'success/',
            cancel_url=YOUR_DOMAIN + 'cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })
