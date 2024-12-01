from django.urls import path
from checkout import views

urlpatterns = [
    path('stripe/config', views.strip_config, name='checkout.strip.config'),
    path('stripe', views.strip_transaction, name='checkout.strip'),
    path('paypal', views.paypal_transaction, name='checkout.paypal'),
]
