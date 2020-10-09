from django.conf import settings
from django.contrib.sites.models import Site
from django.urls import reverse
from django.http import JsonResponse
import stripe

 
def build_line_dict(line, base_url):
    return {
        'price_data': {
            'currency': line.price_currency,
            'unit_amount': int(line.unit_price_incl_tax * 100),
            'product_data': {
                'name': line.product.get_title(),
                'images': ['%s%s' % (base_url, img.original.url) for img in line.product.images.all()],
            },
        },
        'quantity': line.quantity,
    }


def build_line_items_array(basket, base_url):
    return [build_line_dict(line, base_url) for line in basket.all_lines()]


def create_checkout_session(basket, host=None):
    """
    Create a checkout session

    A Checkout Session controls what your customer sees in the Stripe-hosted payment page such as line items, 
    the order amount and currency, and acceptable payment methods. 
    Return the Checkout Session's ID in the response to reference the Session on the client.
    """

    if basket.currency:
        currency = basket.currency
    else:
        currency = getattr(settings, 'STRIPE_CURRENCY', 'GBP')

    if host is None:
        host = Site.objects.get_current().domain

    use_https = getattr(settings, 'STRIPE_CALLBACK_HTTPS', False)
    scheme = 'https' if use_https else 'http'
    base_url = '%s://%s' % (scheme, host)
    success_url = '%s%s' % (base_url, reverse(
        'stripe-success-response', kwargs={'basket_id': basket.id}))
    cancel_url = '%s%s' % (base_url, reverse(
        'stripe-cancel-response', kwargs={'basket_id': basket.id}))
    print(success_url, cancel_url)
    payment_method_types = getattr(settings, 'STRIPE_CALLBACK_HTTPS', ['card'])
    amount = int(basket.total_incl_tax * 100)
    try:
        stripe.api_key = getattr(settings, 'STRIPE_API_KEY', 'sk_test_4eC39HqLyjWDarjtT1zdp7dc')
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=payment_method_types,
            line_items=build_line_items_array(basket, base_url),
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return JsonResponse({'id': checkout_session.id})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=403)
