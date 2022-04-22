from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    featured = models.BooleanField(default=0)
    addition_date = models.DateTimeField(auto_now_add=True, null=True)
    updation_date = models.DateTimeField(auto_now=True, null=True)
    category_image = models.ImageField(upload_to='categoryimages', blank=True, null=True)

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    catid = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcatname = models.CharField(max_length=100)
    subcatdescription = models.TextField(max_length=500)
    subcategory_image = models.ImageField(upload_to='subcatimages', blank=True, null=True)

    def __str__(self):
        return self.subcatname


class Product(models.Model):
    catid = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcatid = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    productname = models.CharField(max_length=100)
    productdescription = RichTextField(max_length=5000)
    price = models.IntegerField()
    product_image1 = models.ImageField(upload_to='productimages', blank=True, null=True)
    product_image2 = models.ImageField(upload_to='productimages', blank=True, null=True)
    product_image3 = models.ImageField(upload_to='productimages', blank=True, null=True)
    discount = models.IntegerField(null=True)

    def __str__(self):
        return self.productname


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    sessionid = models.CharField(max_length=200)
    discountedrate = models.IntegerField(default=0)
    totalcost = models.IntegerField(default=0)


class Orders(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    zipcode = models.IntegerField()
    address = models.CharField(max_length=500)
    payment_options = (('wallet', 'Paytm/GooglePay'),
    ('bank', 'Bank Deposit'),)
    payment_mode = models.CharField(max_length=15, choices=payment_options)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    order_update_options = (('Order Pending', 'Order is pending'),
                             ('In Process', 'Order in Process'),
                            ('Order Shipped', 'Order Shipped'),  ('Order completed', 'Order Completed'),)
    order_status = models.CharField(default='pending', max_length=20, choices=order_update_options)
    total_amount = models.IntegerField(default=0)
    def __str__(self):
        return str(self.id)

class OrderDetails(models.Model):
    orderno = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)
    discountedrate = models.IntegerField(default=0)
    totalcost = models.IntegerField(default=0)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    orderdate = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return str(self.id)