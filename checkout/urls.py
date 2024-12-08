from django.urls import path
from checkout import views
from checkout import webhooks
from paypal.standard.ipn.views import ipn

urlpatterns = [
    path('stripe/config', views.strip_config, name='checkout.strip.config'),
    path('stripe/webhook', webhooks.stripe_webhook),
    path('stripe', views.strip_transaction, name='checkout.strip'),
    path('paypal', views.paypal_transaction, name='checkout.paypal'),
    path('paypal/webhook', ipn, name='checkout.paypal-webhook'),
]
