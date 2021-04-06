from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views import View
#import stripe 
from .models import Chore, Driver, Customer
#stripe.api_key = settings.STRIPE_SECRET_KEY


# IMPORTANT:  UNBLOCK 'stripe' stuff above when ready to test it

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

### ACCESS RIGHTS ###
def register(request):
    if request.POST['startup_owner'] == 'driver':
        errors = Driver.objects.user_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            driver = Driver.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email_address = request.POST['email_address'],
                phone = request.POST['phone'],
                street = request.POST['street'],
                # street2 = request.POST['street2'], # we agreed not to use 'street2'
                city = request.POST['city'],
                state = request.POST['state'],
                zip_code = request.POST['zip_code'],
                # user_lvl = request.POST['user_lvl'], # we may need to think this through in terms of how we collect this data
                photo = request.POST['photo'],  # person creating this feature should tell us what goes here
                password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            )
            request.session['driver_id'] = driver.id
            request.session['greeting'] = driver.first_name
            return redirect('/driver_dash')

    
    if request.POST['startup_owner'] == 'customer':
        errors = Customer.objects.user_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            customer = Customer.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email_address = request.POST['email_address'],
                phone = request.POST['phone'],
                street = request.POST['street'],
                city = request.POST['city'],
                state = request.POST['state'],
                zip_code = request.POST['zip_code'],
                # user_lvl = request.POST['user_lvl'], # we may need to think this through in terms of how we collect this data
                photo = request.POST['photo'],  # person creating this feature should tell us what goes here
                password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            )
            request.session['customer_id'] = customer.id
            request.session['greeting'] = customer.first_name
            return redirect('/customer_dash')


def login(request):
    if request.POST['startup_owner'] == 'customer':
        errors = Customer.objects.login_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            customer = Customer.objects.get(email=request.POST['login_email'])  # note that here I went with 'login_email', not with email_address
            request.session['customer_id'] = customer.id
            request.session['greeting'] = customer.first_name
            context = {
            }
            return render(request, 'customer_dash.html', context)

    if request.POST['startup_owner'] == 'driver':
        errors = Driver.objects.login_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            driver = Driver.objects.get(email=request.POST['login_email'])  # note that here I went with 'login_email', not with email_address
            request.session['driver_id'] = driver.id
            request.session['greeting'] = driver.first_name
            context = {            
            }
            return render(request, 'driver_dash.html', context)

def customer_dash(request):

    return render(request, 'user_dash.html', context)

def driver_dash(request):

    return render(request, 'driver_dash.html', context)