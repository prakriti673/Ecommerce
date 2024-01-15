import json
from .models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        print("CART:",cart)

    items = []
    order = {'get_order_total':0, 'get_order_quantity':0 ,'shipping':False}
    cartItems = order['get_order_quantity']
    
    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_order_total'] += total
            order['get_order_quantity'] += cart[i]["quantity"]

            item = {
                    'product':{
                    'id':product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL':product.imageURL,
                    },
                    'quantity':cart[i]['quantity'],
                    'get_total':total,
                }
            items.append(item)
            
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    
    return {'items':items, 'order':order, 'cartItems':cartItems }

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created=Order.objects.get_or_create(customer = customer,complete=False)
        #set of all ordered items having parent order as order
        items=order.orderitem_set.all() 
        cartItems = order.get_order_quantity
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItems = cookieData['cartItems']
    return {'items':items, 'order':order, 'cartItems':cartItems }
    
def guestOrder(request,data):
    print('User not logged in..')

    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData= cookieCart(request)
    items=cookieData['items']
        
    customer,created = Customer.objects.get_or_create(
        email=email,   
    )
    customer.name=name
    customer.save()

    order=Order.objects.create(
        customer=customer,
        complete=False,
    )
    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product = product,
            order = order,
            # manage for negative cart qty.
            quantity = (item['quantity'] if item['quantity']>0 else -1*item['quantity']),
        )
    
    return customer, order