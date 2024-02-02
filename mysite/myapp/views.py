from django.shortcuts import render, reverse, get_object_or_404, redirect
from .models import Product, OrderDetail
from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse, HttpResponseNotFound
from .forms import ProductForm, UserRegistrationForm
import random
from django.db.models import Sum
import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    products = Product.objects.all()
    user = request.user

    return render(request, "myapp/index.html", {'products': products, 'user': user})


def detail(request, id):
    product = Product.objects.get(id=id)
    stripe_publishable_key = settings.STRIPE_PUBLISHABLE_KEY

    return render(request, 'myapp/detail.html', {'product': product, 'stripe_publishable_key': stripe_publishable_key})


# to make a cross site request that is normally disallowed in django, need the decorator ...
@csrf_exempt
def create_checkout_session(request, id):
    request_data = json.loads(request.body)
    product = Product.objects.get(id=id)

    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        customer_email = request_data.get('email', '').strip(),
        payment_method_types = ['card'],
        line_items=[
            {
                'price_data':{
                    'currency': 'usd',
                    'product_data':{
                        'name':product.name,
                    },
                    'unit_amount': int(product.price * 100)
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url = request.build_absolute_uri(reverse('success')) +
        "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url = request.build_absolute_uri(reverse('failed')),
        # above two, the url the user will be directed to if it is successful / fails
    )

    order = OrderDetail()
    order.customer_email = request_data['email']
    order.product = product
    order.stripe_payment_intent = checkout_session['payment_intent'] # checkout_session object is created using the stripe.checkout.Session.create method, which has the 'payment_intent' attribute
    order.amount = int(product.price)
    order.save()

    return JsonResponse({'sessionId': checkout_session.id}) # returns a JSON response to the client, specifically a dictionary with the key 'sessionId' that will be converted to JSON. Purpose of this is to provide the client with the sessionId associated with the newly created checkout session 


def payment_success_view(request):
    session_id = request.GET.get('session_id') # i.e. the CHECKOUT_SESSION_ID if successful
    if session_id is None:
        return HttpResponseNotFound()
    
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id) # retrieving the order ia the session_id
    order = get_object_or_404(OrderDetail,stripe_payment_intent = session.payment_intent) # getting the order via the stripe payment_intent identifier

    order.has_paid = True

    # updating sales stats for the product
    product = Product.objects.get(id=order.product.id)
    product.total_sales_amount += int(product.price)
    product.total_sales += 1
    product.save()

    order.save()

    return render(request, 'myapp/payment_success.html', {'order': order})


def payment_failed_view(request):
    return render(request, 'myapp/failed.html')

@login_required
def create_product(request):

    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES) # gives you all the data in the submitted form, then the files
        if product_form.is_valid():
            new_product = product_form.save(commit=False) # saves it as an object, but doesn't save to the database yet
            new_product.seller = request.user # logged in user making the request
            new_product.save() # saves as a Product, as the ProductForm is based on creating a new Product model
            return redirect('index')

    product_form = ProductForm()
    return render(request, 'myapp/create_product.html', {'product_form': product_form})

@login_required
def product_edit(request,id):
    product = Product.objects.get(id=id)

    # adding a check, if the logged in user is not the seller, cannot perform operation
    if not (request.user.is_superuser or product.seller == request.user):
        return redirect('invalid')

    product_form = ProductForm(request.POST or None, request.FILES or None, instance=product) # will take the product data and fill the form with it
    # above, or None used e.g. if it's a get request will not be data in the request.POST dictionary, so will be the initial product.
    # BUT if there is a post request, will use the request.POST and request.FILES (i.e. inputted data) then enter the if statement below to save it etc
    
    if request.method == "POST":
        if product_form.is_valid():
            product_form.save()
            return redirect('index')

    return render(request, 'myapp/product_edit.html', {'product_form': product_form, 'product': product})

@login_required
def product_delete(request,id):
    product = Product.objects.get(id=id)

    if not (request.user.is_superuser or product.seller == request.user):
        return redirect('invalid')

    if request.method == "POST":
        product.delete()
        return redirect('index')

    return render(request, 'myapp/delete.html', {'product': product})


# dashboard view
@login_required
def dashboard(request):
    if request.user.is_superuser:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(seller=request.user)
    
    # randomly generating rating
    for product in products:
        product.random_rating = round(random.uniform(0.0, 5.0), 1)

    return render(request, 'myapp/dashboard.html', {'products': products})


# registration view
def register(request):

    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST) # user_form is the form with the data from request.POST, i.e. inputted data
        
        # saving data and adding passwords, then saving user
        new_user = user_form.save(commit=False) # .save() method would only save the fields in the fields array in the form 
        new_user.set_password(user_form.cleaned_data['password'])    
        new_user.save()
        return redirect('index') # need to change to log in page, but not yet created

    user_form = UserRegistrationForm()
    return render(request, 'myapp/register.html', {'user_form': user_form})


# invalid view (e.g. if trying to access edit or delete operations on other sellers products)
def invalid(request):
    return render(request, 'myapp/invalid.html')


# my purchases view
@login_required
def my_purchases(request):

    if request.user.is_superuser:
        orders = OrderDetail.objects.all()
    else:
        orders = OrderDetail.objects.filter(customer_email=request.user.email)

    return render(request, 'myapp/purchases.html', {'orders': orders})


# sales dashboard view
@login_required
def sales(request):

    if request.user.is_superuser:
        orders = OrderDetail.objects.all()
    else:
        orders = OrderDetail.objects.filter(product__seller=request.user) # __ syntax for getting the product field of OrderDetail, a foreign key for Product, then accessing the .seller property of the Product model

    total_sales = orders.aggregate(Sum('amount')) # taking Sum of the 'amount' field
    user = request.user

    # import datetime
    # calculating last year's sales sum
    last_year = datetime.date.today() - datetime.timedelta(days=365) # i.e. today minus 365
    last_year_orders = orders.filter(created_on__gt=last_year) # filtering the orders object, due to the above if else statements still want to apply the user restriction unless its the superuser
    yearly_sales = last_year_orders.aggregate(Sum('amount'))

    # calculating last year's (last 365 days) sales sum
    last_year = datetime.date.today() - datetime.timedelta(days=365) # i.e. today minus 365
    last_year_orders = orders.filter(created_on__gt=last_year) # filtering the orders object, due to the above if else statements still want to apply the user restriction unless its the superuser
    yearly_sales = last_year_orders.aggregate(Sum('amount'))

    # calculating last 30 days sales sum
    last_year = datetime.date.today() - datetime.timedelta(days=30) 
    last_year_orders = orders.filter(created_on__gt=last_year) 
    monthly_sales = last_year_orders.aggregate(Sum('amount'))

    # calculating last 7 days sales sum
    last_year = datetime.date.today() - datetime.timedelta(days=7) 
    last_year_orders = orders.filter(created_on__gt=last_year) 
    weekly_sales = last_year_orders.aggregate(Sum('amount'))

    # everyday sum for each day for the past 30 days
    daily_sales_sums = orders.values('created_on__date').order_by('created_on__date').annotate(sum=Sum('amount'))
    # now daily_sales_sums will be an object list, e.g. <QuerySet [{'sum': 355, 'created_on__date': datetime.date(2024, 2, 1)}]>

    # sales sum per product (similar to above, will produce an object list)
    product_sales_sums = orders.values('product__name').order_by('product__name').annotate(sum=Sum('amount'))
    print(product_sales_sums)

    return render(request, 'myapp/sales.html', {'orders': orders, 'total_sales': total_sales, 'user': user, 'yearly_sales': yearly_sales, 'monthly_sales':monthly_sales, 'weekly_sales': weekly_sales, 'daily_sales_sums': daily_sales_sums, 'product_sales_sums':product_sales_sums})
