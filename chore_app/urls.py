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
    path("register", views.register),
    path("login", views.login),
]