from django.urls import path, include
from . import views
from chore_app.views import (
    CreateCheckoutSessionView,
    ChoreLandingPageView
)

urlpatterns = [
    path('', views.index, name ='home'),
    path('landing/', ChoreLandingPageView.as_view(), name = 'landing-page'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('base/', views.base, name='base'),
    path('register', views.register),  # DONE
    path('login', views.login),  # DONE
    path('customer_dash', views.customer_dash),
    path('driver_dash', views.driver_dash),
]