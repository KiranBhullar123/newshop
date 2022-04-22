import json
import urllib

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMultiAlternatives

from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from newshopapp.forms import MyLoginForm, RegisterForm
from newshopapp.models import Category, SubCategory, Product, Cart, Orders, OrderDetails
from newshopsite import settings
from newshopsite.settings import API_KEY


def my_index(request):
    source = urllib.request.urlopen(
        'https://api.openweathermap.org/data/2.5/weather?q=Batala,In&appid=' + API_KEY + '&units=metric').read()
    # converting JSON data to a dictionary
    list_of_data = json.loads(source)

    # data for variable list_of_data
    data = {
        "temp": str(list_of_data['main']['temp']),
        "forecast": str(list_of_data['weather'][0]['description'])
    }

    categorydata = Category.objects.all()
    return render(request, "index.html", {"mycategories": categorydata, "tempdata": data})

def show_subcategories(request, cid):
    subcatdata = SubCategory.objects.filter(catid=cid)
    return render(request, "subcategories.html", {"subcategorydata" : subcatdata})

def show_products(request):
    mysubcatid = request.GET.get("subcatid")
    mycatid = request.GET.get("catid")
    productdata = Product.objects.filter(catid=mycatid, subcatid=mysubcatid)
    return render(request, "products.html", {"productsdata" : productdata})
def productdetails(request, pid):
    productdetaildata = Product.objects.get(id=pid)
    discount = productdetaildata.discount
    originalprice = productdetaildata.price
    discountedprice = round(originalprice - (discount * originalprice) / 100)
    return render(request, "product_detail.html",
                  {"productdetaildata": productdetaildata, "discountedprice": discountedprice})

def addtocart(request):
    productid = request.POST.get("productid")
    if not request.session or not request.session.session_key:
        request.session.save()
        SESSION_KEY = request.session.session_key
        request.session["sid"] = SESSION_KEY
    else:
        if 'sid' in request.session:
            SESSION_KEY = request.session["sid"]
        else:
            SESSION_KEY = request.session.session_key
    request.session["sid"] = SESSION_KEY
    qty = request.POST.get("quantity")

    oldcart = Cart.objects.filter(product=productid, sessionid=SESSION_KEY).first()
    if oldcart:
        qty = int(oldcart.qty) + int(qty)
        totalcost = int(oldcart.discountedrate) * int(qty)
        Cart.objects.filter(product=productid, sessionid=SESSION_KEY).update(qty=qty, totalcost=totalcost)
    else:
        discountedrate = request.POST.get("discountedrate")
        totalcost = int(discountedrate) * int(qty)

        cartobj = Cart()
        cartobj.product = Product(productid)
        cartobj.totalcost = totalcost
        cartobj.discountedrate = discountedrate
        cartobj.qty = qty
        cartobj.sessionid = SESSION_KEY
        cartobj.save()
    return HttpResponseRedirect(reverse('showcart'))
def showcart(request):
    if not request.session or not request.session.session_key:
        sessionid = request.session.session_key
    else:
        if 'sid' in request.session:
            sessionid = request.session["sid"]
        else:
            sessionid = request.session.session_key
    cartdata = Cart.objects.filter(sessionid=sessionid)
    cartsum = Cart.objects.filter(sessionid=sessionid).aggregate(Sum('totalcost'))
    return render(request, "cart.html", {"cartdata": cartdata, "cartsum": cartsum})


# def showcart(request):
#     cartdata = Cart.objects.filter(sessionid=request.session.session_key)
#     cartsum = Cart.objects.filter(sessionid=request.session.session_key).aggregate(Sum('totalcost'))
#
#     return render(request,"cart.html",{"cartdata":cartdata,"cartsum":cartsum})
def deleteitemincart(request, pid):
    if not request.session or not request.session.session_key:
        sessionid = request.session.session_key
    else:
        if 'sid' in request.session:
            sessionid = request.session["sid"]
        else:
            sessionid = request.session.session_key
    Cart.objects.filter(product=pid, sessionid=sessionid).delete()
    return HttpResponseRedirect(reverse('showcart'))

@login_required()
def checkout(request):
    sessionid = request.session["sid"]
    cartdata = Cart.objects.filter(sessionid=sessionid)
    cartsum = Cart.objects.filter(sessionid=sessionid).aggregate(Sum('totalcost'))

    return render(request, "checkout.html", {"cartdata": cartdata, "cartsum": cartsum})
@login_required()
def do_checkout(request):
    mycheckoutform = Orders()
    name = request.POST.get("name")
    email = request.POST.get("email")
    phone = request.POST.get("phone")
    address = request.POST.get("address")
    zipcode = request.POST.get("zipcode")
    paymentmode = request.POST.get("paymentmode")
    totalamt = request.POST.get("totalcost")
    mycheckoutform.name = name
    mycheckoutform.email = email
    mycheckoutform.phone = phone
    mycheckoutform.address = address
    mycheckoutform.zipcode = zipcode
    mycheckoutform.payment_mode = paymentmode
    mycheckoutform.total_amount = totalamt
    mycheckoutform.username = User.objects.get(username=request.session["myname"])
    mycheckoutform.save()
    orderno = Orders.objects.latest('id')
    if not request.session or not request.session.session_key:
        sessionid = request.session.session_key
    else:
        sessionid = request.session["sid"]
    for mycartdata in Cart.objects.filter(sessionid=sessionid):
        orderdetailobj = OrderDetails()
        orderdetailobj.orderno = orderno
        orderdetailobj.qty = mycartdata.qty
        orderdetailobj.discountedrate = mycartdata.discountedrate
        orderdetailobj.totalcost = mycartdata.totalcost
        orderdetailobj.product = Product(mycartdata.product.id)
        orderdetailobj.username = User.objects.get(username=request.session["myname"])
        orderdetailobj.save()
    Cart.objects.filter(sessionid=sessionid).delete()
    message = EmailMultiAlternatives(
        'Message from Shop',
        'Congrats! You have got a new order',
        to=["kb788489@gmail.com"],  # where you receive the contact emails
        from_email=settings.EMAIL_HOST_USER,
        reply_to=['kb788489@gmail.com'])
    result = message.send(fail_silently=False)
    return render(request, "order-success.html", {"orderno": orderno, "result": result})









def my_login(request):
    myloginform = MyLoginForm(request.POST or None)
    if myloginform.is_valid():
        username = myloginform.cleaned_data.get("uname")  # got username from login form
        redirect_to = request.POST.get('next')
        userobj = User.objects.get(username__iexact=username)  # return userobj with help of username
        login(request, userobj)  # session create
        request.session["myname"] = username  # variable stored in session
        if redirect_to:
            return redirect(redirect_to)
        else:
            return HttpResponseRedirect(reverse("home"))
    else:
       return render(request, "login.html", {"meraloginform": myloginform})


def showorders(request):
    userobj = User.objects.get(username=request.session["myname"])
    ordersdata = Orders.objects.filter(username=userobj)
    return render(request, "orders.html", {"ordersdata": ordersdata})
def showorderdetails(request, id):
    orderdetailsdata = OrderDetails.objects.filter(orderno=id)
    return render(request, "order-history.html", {"orderdetailsdata": orderdetailsdata})


class my_signup(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = 'signup.html'
    success_url = reverse_lazy('usersignup')
    success_message = "Your account has been created successfully. You can login now"

    def dispatch(self, *args, **kwargs):
        return super(my_signup, self).dispatch(*args, **kwargs)

def my_signout(request):
    logout(request)  # session destroy
    categorydata = Category.objects.all()
    return render(request, "index.html", {"mycategories": categorydata})
def changepassword(request):
    if request.method == "POST":
        myformdata = request.POST
        oldpassword = myformdata.get("oldpassword", "0")
        newpass1 = myformdata.get("password1", "1")
        newpass2 = myformdata.get("password2", "2")
        if newpass1 == newpass2:
            myusername = request.session["myname"]
            userobj = authenticate(username=myusername, password=oldpassword)
            if userobj is not None:
                userobj.set_password(newpass2)
                userobj.save()
                logout(request)
                messages.success(request, 'Password changed successfully. Login again')
                return HttpResponseRedirect(reverse('userlogin'))
            else:
                messages.error(request, 'Wrong old password')
                return render(request, "changepassword.html")
        else:
            messages.error(request, 'New Passwords does not match')
            return render(request, "changepassword.html")
    else:
        return render(request, "changepassword.html")
def searchproduct(request):
    if request.method == "POST":
        search_term = request.POST.get("searchterm")
        searchdata = Product.objects.filter(productname__icontains=search_term)
        return render(request, "searchresults.html", {"searchdata": searchdata})
