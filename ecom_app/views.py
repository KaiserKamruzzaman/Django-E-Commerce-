from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
import datetime
import json
from .utils import cookieCart, cartData, guestOrder
from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator


# Create your views here.
def store(request):
    # products=Product.objects.all()
    # products=Paginator(products,6)
    # context={'products':products}
    # return render(request,'ecom_app/store.html',context)

    data=cartData(request)
    cart_items=data['cart_items']

    products=Product.objects.all()
    paginator=Paginator(products,3)

    page_number=request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context={'page_obj':page_obj, 'cart_items':cart_items}
    return render(request,'ecom_app/store.html',context)

def cart(request):
    data=cartData(request)
    cart_items=data['cart_items']
    order=data['order']
    items=data['items']

    context={'items':items, 'order':order, 'cart_items':cart_items}
    return render(request,'ecom_app/cart.html',context)

def checkout(request):
    data=cartData(request)
    cart_items=data['cart_items']
    order=data['order']
    items=data['items']

    context={'items':items, 'order':order, 'cart_items':cart_items}
    return render(request,'ecom_app/checkout.html',context)

def updateItem(request):
    product_id=request.POST.get('product_id')
    product_action=request.POST.get('product_action')
    customer=request.user.customer
    product=Product.objects.get(id=product_id)
    order, created=Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created=OrderItem.objects.get_or_create(order=order, product=product)

    if product_action=='add':
        orderItem.quantity+=1
    else:
        orderItem.quantity-=1
    orderItem.save()
    if orderItem.quantity <=0:
        orderItem.delete()

    cart_count=order.total_cart_items

    return JsonResponse({'success':'Product added Successfully!!!','order_id':order.id,'cart_count':cart_count,'shipping':False})

def process_order(request):
    address=request.POST.get('address')
    city=request.POST.get('city')
    state=request.POST.get('state')
    zip_code=request.POST.get('zip_code')
    country=request.POST.get('country')
    total_amount=float(request.POST.get('total_amount'))
    # example of dynamic transaction_id
    transaction_id=datetime.datetime.now().timestamp()


    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer,order=guestOrder(request)

    order.transaction_id=transaction_id
    if total_amount == order.total_cart_amount:
        order.complete=True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(customer=customer,order=order,
                                    address=address,city=city,state=state,
                                    zip_code=zip_code,country=country)

    return JsonResponse({'success':'Order Placed Successfully!!!'})

def userLogin(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('ecom_app:store')
        else:
            messages.info(request, 'Invalid UserName or Password!!')
            return redirect('ecom_app:userLogin')

    return render(request,'ecom_app/login.html')

def userLogout(request):
    logout(request)
    return redirect('ecom_app:store')

def register(request):
    form=CreateUserForm()
    if request.method == 'POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user_name=form.cleaned_data.get('username')
            form.save()
            cus_user=User.objects.get(username=user_name)
            Customer.objects.create(user=cus_user,name=cus_user,email=cus_user.email)
            messages.success(request, 'New Account was created named: '+user_name)
            return redirect('ecom_app:userLogin')


    context={'form':form}
    return render(request,'ecom_app/register.html',context)
