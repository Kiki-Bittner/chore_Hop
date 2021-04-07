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
    path('customer_dash/<int:customer_id>', views.customer_dash),
    path('new_chore/<int:customer_id>', views.new_chore),
    path('driver_dash/<int:driver_id>', views.driver_dash),
    path('driver_chore', views.driver_chore),
    path('user_chore/<int:chore_id>', views.user_chore),
    path('delete_chore/<int:customer_id>/<int:chore_id>', views.delete_chore),
    path('claim_chore/<int:driver_id>', views.claim_chore),
    path("logout", views.logout),  # DONE
]
