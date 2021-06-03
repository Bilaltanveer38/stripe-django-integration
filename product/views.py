from django.conf import settings
from django.views import View
from django.core.mail import send_mail
from .models import Product
from django.views.generic.base import TemplateView
import stripe
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

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
            metadata={"product_id": product.id},
            mode='payment',
            success_url=YOUR_DOMAIN + 'success/',
            cancel_url=YOUR_DOMAIN + 'cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK
        )
    except ValueError:
        # e = None

        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:

        # Invalid signature
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fulfill the purchase...
        fulfill_order(session)

    elif event['type'] == 'charge.failed':
        session = event['data']['object']
        # Send an email to the customer asking them to retry their order
        email_customer_about_failed_payment(session)

        # Fulfill the purchase...
    # Passed signature verification

    return HttpResponse(status=200)


def fulfill_order(session):
    customer_email = session['customer_details']['email']
    product_id = session['metadata']['product_id']

    print(customer_email + product_id)
    product = Product.objects.get(pk=product_id)

    send_mail(subject='Thank you for the purchase',
              message=f'Thank you for the purchase, your order is here. Please click the link: {product.url} '
                      f'to access it',
              from_email='matt@gmail.com',
              recipient_list=[customer_email]
              )


def email_customer_about_failed_payment(session):
    print(session['billing_details']['email'] + ' ' + session['billing_details']['name'] + ' ' + session['failure_code'])


class StripeIntentView(View):
    def post(self, *args, **kwargs):
        try:
            pk = self.kwargs['pk']
            product = Product.objects.get(pk=pk)
            intent = stripe.PaymentIntent.create(
                amount=product.price,
                currency='usd'
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, 403)