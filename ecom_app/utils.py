import json
from .models import *

def cookieCart(request):
    try:
        cart=json.loads(request.COOKIES['cart'])
    except:
        cart={}

    items=[]
    order={'total_cart_items':0,'total_cart_amount':0,'shipping':False}
    cart_items=order['total_cart_items']
    for i in cart:
        try:
            cart_items += cart[i]['quantity']
            product=Product.objects.get(id=i)
            total=(product.price * cart[i]['quantity'])
            order['total_cart_amount'] += total
            order['total_cart_items'] += cart[i]['quantity']

            item={
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,

                },
                'quantity':cart[i]['quantity'],
                'get_total':total,
            }
            items.append(item)
            if product.digital == False:
                order['shipping']=True
        except:
            pass
    return { 'cart_items':cart_items, 'order':order, 'items':items }

def cartData(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created=Order.objects.get_or_create(customer=customer, complete=False)
        items=order.orderitem_set.all()
        cart_items=order.total_cart_items
    else:
        cookie_data=cookieCart(request)
        cart_items=cookie_data['cart_items']
        order=cookie_data['order']
        items=cookie_data['items']
    return {'items':items, 'order':order, 'cart_items':cart_items}

def guestOrder(request):
    print('User is not logged in...')
    name=request.POST.get('user_name')
    email=request.POST.get('user_email')
    cookieData=cookieCart(request)
    items=cookieData['items']

    customer,created=Customer.objects.get_or_create(email=email)
    customer.name=name
    customer.save()

    order=Order.objects.create(customer=customer,complete=False)

    for item in items:
        product=Product.objects.get(id=item['product']['id'])
        order_items=OrderItem.objects.create(product=product,order=order,quantity=item['quantity'])

    return customer,order
