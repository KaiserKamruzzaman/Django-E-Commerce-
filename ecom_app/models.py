from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name=models.CharField(max_length=254, null=True)
    email=models.EmailField(max_length=254, null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=254)
    price=models.FloatField(null=True)
    digital=models.BooleanField(default=False, null=True, blank=True)
    image=models.ImageField(upload_to='product_pics', null=True)
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
    customer=models.ForeignKey(Customer,null=True, blank=True, on_delete=models.CASCADE)
    date_order=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False)
    transaction_id=models.CharField(max_length=100, null=True)
    def __str__(self):
        return f'{str(self.id)}---{self.customer.name}'

    @property
    def total_cart_items(self):
        order_items=self.orderitem_set.all()
        total=0
        for item in order_items:
            total+=item.quantity
        return total

    @property
    def total_cart_amount(self):
        order_items=self.orderitem_set.all()
        total=0
        for item in order_items:
            total+=item.get_total
        return total
    @property
    def shipping(self):
        shipping=False
        order_items=self.orderitem_set.all()
        for item in order_items:
            if item.product.digital == False:
                shipping=True
        return shipping


class OrderItem(models.Model):
    product=models.ForeignKey(Product,null=True, blank=True, on_delete=models.CASCADE)
    order=models.ForeignKey(Order,null=True, blank=True, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0, null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        # return self.product.name
        return f'{self.product.name}---order{self.order.id}'

    @property
    def get_total(self):
        total=(self.product.price*self.quantity)
        return total

class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,null=True, blank=True, on_delete=models.SET_NULL)
    order=models.ForeignKey(Order,null=True, blank=True, on_delete=models.SET_NULL)
    address=models.CharField(max_length=254, null=False)
    city=models.CharField(max_length=254, null=False)
    state=models.CharField(max_length=254, null=False)
    zip_code=models.CharField(max_length=254, null=False)
    country=models.CharField(max_length=254, null=False)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address
