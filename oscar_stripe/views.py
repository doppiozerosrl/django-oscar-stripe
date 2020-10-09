from oscar_stripe.facade import create_checkout_session
from oscar.core.loading import get_model, get_class
from django.shortcuts import redirect
from django.urls import reverse

Basket = get_model('basket', 'Basket')
Selector = get_class('partner.strategy', 'Selector')


def success_url(request, basket_id):
    print('success')
    return redirect(reverse("checkout:shipping-address"))

def cancel_url(request, basket_id):
    print('cancel')
    return redirect(reverse("checkout:shipping-address"))

def create_session(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    if not basket.has_strategy:
        basket.strategy = Selector().strategy(request)
    return create_checkout_session(basket)