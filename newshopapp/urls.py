from django.conf.urls.static import static
from django.urls import path

from newshopapp import views
from newshopsite import settings

urlpatterns = [
    path('', views.my_index, name='home'),
    path('user-login', views.my_login, name='userlogin'),
    path('user-registration', views.my_signup.as_view(), name='usersignup'),
    path('user-logout', views.my_signout, name='signout'),
    path('sub-categories/<int:cid>', views.show_subcategories, name='subcategories'),
    path('products', views.show_products, name='products'),
    path('products-info/<int:pid>', views.productdetails, name='details'),
    path('delete-in-cart/<int:pid>', views.deleteitemincart,name='deleteitem' ),
    path('addtocart', views.addtocart, name='addtocart'),
    path('shopping-cart', views.showcart, name='showcart'),
    path('checkout', views.checkout, name='checkout'),
    path('order-checkout', views.do_checkout, name='order'),
    path('order-history', views.showorders, name='showorders'),
    path('order-details/<int:id>', views.showorderdetails, name='orderdetails'),
    path('change-password', views.changepassword, name='changepassword'),
    path('search-product', views.searchproduct, name='searchproduct'),







] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
