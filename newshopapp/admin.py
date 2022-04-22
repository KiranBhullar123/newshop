from django.contrib import admin

# Register your models here.
from newshopapp.models import Category, SubCategory, Product, Orders, OrderDetails


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'description']

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['subcatname', 'subcatdescription']

@admin.register(Product)
class MyProductAdmin(admin.ModelAdmin):
    list_display = ['productname', 'productdescription','price','catid', 'subcatid']

@admin.register(Orders)
class MyOrders(admin.ModelAdmin):
    list_display = ['id', 'name','email','phone', 'zipcode', 'address', 'payment_mode', 'username', 'order_status']


@admin.register(OrderDetails)
class OrderDetails(admin.ModelAdmin):
    list_display = ['orderno', 'product','qty','discountedrate', 'totalcost']


