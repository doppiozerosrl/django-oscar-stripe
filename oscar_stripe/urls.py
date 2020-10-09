from django.urls import path
from oscar_stripe import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [ 
    path('success/<int:basket_id>', csrf_exempt(views.success_url), name='stripe-success-response'),
    path('cancel/<int:basket_id>', csrf_exempt(views.cancel_url), name='stripe-cancel-response'),
    path('create-session/<int:basket_id>', csrf_exempt(views.create_session), name='stripe-create-session'),
]
