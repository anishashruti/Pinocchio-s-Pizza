from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from orders.models import (Dinnerplatter, Pasta, Regular_pizza, Salad, Sub,Sicilian_pizza,
                           Topping,Order2)
from users.models import UserOrders
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages
from django.views.generic import ListView
from django.conf import settings
import stripe
from orders.extras import generate_order_id, transact, generate_client_token

stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.

n=[]
n=list(Order2.objects.all())

def home(request):
    return render(request, "orders/home.html",{'title':'Home'})

def menu(request):
    context = {
        "pastas": Pasta.objects.all(),
        "salads": Salad.objects.all(),
        "platters": Dinnerplatter.objects.all(),
    }

    return render(request, "orders/menu.html",context)
def menu1(request):

    context = {
        "subs": Sub.objects.all(),
    }

    return render(request, "orders/sub.html",context)

def pizza(request):
    context = {
        "S_pizzas":Sicilian_pizza.objects.all(),
        "R_pizzas": Regular_pizza.objects.all(),
        "toppings":Topping.objects.all()
    }

    return render(request, "orders/pizza.html",context)

def about(request):
    return render(request, "orders/about.html",{'title':'About'})

def toppings(request,category,name):
    context = {
        "toppings":Topping.objects.all()
    }

    return render(request, "orders/toppings.html",context)


@login_required(login_url='/login/')
def add(request,category,size,name,price):
    o=Order2()
    user = User.objects.get(id=request.user.id)
    o.user=user
    o.name=name
    o.size=size
    o.price=price
    o.category=category
    o.save()    
    messages.success(request,'Order added to cart. ')
    return redirect(reverse('menu'))

def delete(request,category,size,name,price):

    find_order=Order2.objects.filter(user=request.user,category=category,name=name,price=price)[0]
    find_order.delete() 

    messages.success(request,'Order successfully deleted. ')
    return redirect('menu')

def order_placed(request):
    
    context = {
        "orders":Order2.objects.all(),
    }
    return render(request, "orders/myorders.html",context)


class user_order_list_view(ListView):
    model = Order2

    template_name='orders/Mycart.html'
    context_object_name='Order2'
    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Order2.objects.filter(user=user)

def get_user_pending_order(request):
    # get order for the correct user
    order = Order2.objects.filter(user=request.user)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0

@login_required()
def checkout(request, **kwargs):
    client_token = generate_client_token()
    existing_order = get_user_pending_order(request)
    print(existing_order)
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        token = request.POST.get('stripeToken', False)
        if token:
            try:
                charge = stripe.Charge.create(
                    amount=100*existing_order.get_cart_total(request.user),
                    currency='usd',
                    description='Example charge',
                    source=token,
                )

                return 
                
                redirect(reverse('orders:update_records',
                        kwargs={
                            'token': token
                        })
                    )
            except stripe.CardError as e:
                message.info(request, "Your card has been declined.")
        else:
            result = transact({
                'amount': existing_order.get_cart_total(request.user),
                'payment_method_nonce': request.POST['payment_method_nonce'],
                'options': {
                    "submit_for_settlement": True
                }
            })

            if result.is_success or result.transaction:
                messages.success(request,'Payment successfully done ')
                return redirect('success')
            else:
                for x in result.errors.deep_errors:
                    messages.info(request, x)
                return redirect(reverse('orders:checkout'))
            
    context = {
        'order': existing_order,
        'client_token': client_token,
        'STRIPE_PUBLISHABLE_KEY': publishKey
    }

    return render(request, 'orders/checkout.html', context)

def success(request):
    return render(request, "orders/purchase_success.html")



     

