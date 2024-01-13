from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=200, null=True)
    email=models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=200, null=True)
    price=models.DecimalField(max_digits=7, decimal_places=2)
    digital=models.BooleanField(default=False, null=True, blank=False)
    image=models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url

class Order(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False, blank=True,null=True)
    transaction_id=models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id) 
    
    @property
    def get_order_total(self):
        order_total=0
        for o in self.orderitem_set.all() :
            order_total+=o.get_total
        return order_total
    
    @property
    def get_order_quantity(self):
        order_quantity=0
        for o in self.orderitem_set.all() :
            order_quantity+=o.quantity
        return order_quantity
    
    @property
    def shipping(self):
        shipping=False
        orderitems=self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    
# this stores the items inside the cart
class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL, null=True,blank=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    quantity=models.IntegerField(default=0,blank=True,null=True)
    date_added=models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total=self.product.price*self.quantity
        return total

class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    address=models.CharField(max_length=1000, null=False)
    city=models.CharField(max_length=200, null=False)
    state=models.CharField(max_length=200, null=False)
    zipcode=models.CharField(max_length=6, null=False)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    

