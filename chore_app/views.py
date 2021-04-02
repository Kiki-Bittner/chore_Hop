from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views import View
import stripe 
from .models import Chore
stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
    return render(request, 'index.html')

class ChoreLandingPageView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        chore = Chore.objects.get(name="Test Chore")
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            'chore': chore,
            'STRIPE_PUBLIC_KEY': setting.STRIPE_PUBLIC_KEY
        })
        return context

class CreateCheckoutSessionView(View):
    def post(self,request, *args, **kwargs):
        YOUR_DOMAIN ="http://127.0.0.1:8000/",
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 1000,
                        'product_data': {
                            'name': 'Stubborn Attachments',
                            #'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


