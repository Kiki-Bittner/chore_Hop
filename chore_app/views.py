from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views import View
from django.contrib import messages 
from .models import Chore, Driver, Customer
import bcrypt, json, requests

#import stripe
# <<<<<<< HEAD

# <<<<<<< HEAD
def base(request):
    return render(request, 'base.html')
# =======
# =======
# >>>>>>> 867abd9e692c0164ed731f7a5876df6ed00f67c3
# #stripe.api_key = settings.STRIPE_SECRET_KEY


# # IMPORTANT:  UNBLOCK 'stripe' stuff above when ready to test it
# >>>>>>> 9a0c2f409e30f35e1b4e0a71d4be9f5f2f6934d9
geodata = {}

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
        errors = Driver.objects.driver_validator(request.POST)
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
                city = request.POST['city'],
                state = request.POST['state'],
                zip_code = request.POST['zip_code'],
                photo = request.POST['photo'],  # person creating this feature should tell us what goes here
                password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            )
            request.session['driver_id'] = driver.id
            request.session['greeting'] = driver.first_name
            return redirect(f'/driver_dash/{driver.id}')

    
    if request.POST['startup_owner'] == 'customer':
        errors = Customer.objects.customer_validator(request.POST)
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
            return redirect(f'/customer_dash/{customer.id}')


def login(request):
    if request.POST['startup_owner'] == 'customer':
        errors = Customer.objects.login_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            customer = Customer.objects.get(email_address=request.POST['login_email'])  # note that here I went with 'login_email', not with email_address
            request.session['customer_id'] = customer.id
            request.session['greeting'] = customer.first_name
            # context = {
            #     'first_name': Customer.objects.all(),
            # }
            return redirect(f'/customer_dash/{customer.id}')

    if request.POST['startup_owner'] == 'driver':
        errors = Driver.objects.login_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            driver = Driver.objects.get(email_address=request.POST['login_email'])  # note that here I went with 'login_email', not with email_address
            request.session['driver_id'] = driver.id
            request.session['greeting'] = driver.first_name
            # context = {            
            # }
            return redirect(f'/driver_dash/{driver.id}')
# <<<<<<< HEAD
# =======

# >>>>>>> e7a142a4e846c74deda67ed6b0d475337a45b6b9

def customer_dash(request, customer_id):

    context = {
        'current_customer': Customer.objects.get(id=customer_id),
        'customer_chores': Customer.objects.get(id=customer_id).has_customer.all(),  
    }
    return render(request, 'customer_dash.html', context)

def driver_dash(request, driver_id):
    driver = Driver.objects.get(id=request.session['driver_id'])
    customer1 = Customer.objects.get(id=1)
    customer2 = Customer.objects.get(id=2)
    customer3 = Customer.objects.get(id=3)
    maps(driver)
    customer1_coords = maps(customer1)
    customer2_coords = maps(customer2)
    customer3_coords = maps(customer3)
    context = {
        # context is empty for now, so add what you need if you need to add stuff to driver_dash page
        "latitude": geodata['lat'],
        "longitude": geodata['lng'],
        "customer1": customer1,
        "customer2": customer2,
        "customer3": customer3,
        "customer1_coords_lat": customer1_coords['lat'],
        "customer1_coords_lng": customer1_coords['lng'],
        "customer2_coords_lat": customer2_coords['lat'],
        "customer2_coords_lng": customer2_coords['lng'],
        "customer3_coords_lat": customer3_coords['lat'],
        "customer3_coords_lng": customer3_coords['lng'],
        'current_driver': Driver.objects.get(id=driver_id),
        'customer_chores': Chore.objects.all(),
        'driver_chores': Chore.objects.filter(driver=Driver.objects.get(id=driver_id))
    }
    return render(request, 'driver_dash.html', context)

def maps(person):
    GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
    street = person.street
    city = person.city
    state = person.state
    params = {
        'address': f'{street} {city},{state}',
        'key': 'AIzaSyCCVsdD6lPm8vzcsO64fUDxp_pt65hlk4M'
    }
    req = requests.get(GOOGLE_MAPS_API_URL, params=params)
    res = req.json()
    geodata['lat'] = res['results'][0]['geometry']['location']['lat']
    geodata['lng'] = res['results'][0]['geometry']['location']['lng']
    geodata['address'] = res['results'][0]['formatted_address']
    
    return geodata

def driver_chore(request):
    driver = Driver.objects.get(email_address=request.POST['login_email'])
    maps(driver)
    customer1 = Customer.objects.get(id=1)
    customer1_coords = maps(customer1)
    context = {
        "latitude": geodata['lat'],
        "longitude": geodata['lng'],
        "customer1": customer1,
        "customer1_coords_lat": customer1_coords.geodata['lat'],
        "customer1_coords_lng": customer1_coords.geodata['lng'],
    }
    return render(request, 'driver_chore.html', context)

def user_chore(request, chore_id):
    customer = Customer.objects.get(email_address=request.POST['login_email'])
    maps(customer)
    driver1 = Driver.objects.get(id=1)
    driver1_coords = maps(driver1)
    context = {
        "latitude": geodata['lat'],
        "longitude": geodata['lng'],
        "driver1": driver1,
        "driver1_coords_lat": driver1_coords.geodata['lat'],
        "driver1_coords_lng": driver1_coords.geodata['lng'],
    }
    return render(request, 'user_chore.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')


def new_chore(request, customer_id):
    if request.method == "POST":

        current_customer = Customer.objects.get(id=customer_id)

        chore = Chore.objects.create(name=request.POST['name'], description=request.POST['description'], due_date=request.POST['due'], price=request.POST['price'], customer=current_customer)


    return redirect(f'/customer_dash/{customer_id}')

def delete_chore(request, customer_id, chore_id):
    current_customer = Customer.objects.get(id=request.session['customer_id'])
    current_chore = Chore.objects.filter(customer=current_customer)

    c = current_chore.get(id=chore_id)
    c.delete()
    return redirect(f'/customer_dash/{customer_id}')

def claim_chore(request, driver_id, chore_id):
    
    return redirect(f'/driver_dash/{driver_id}')
