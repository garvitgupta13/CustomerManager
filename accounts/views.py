from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory#for multiple form
from django.contrib.auth.forms import UserCreationForm#for Creating a user
from django.contrib import messages #to send flash messages after signup

from django.contrib.auth import authenticate, login, logout #for login, logout

from django.contrib.auth.decorators import login_required #for restricted access

from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
# Create your views here.

def registerPage(request):
    #If user is authennticated then redirect him to 'home' link
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if(request.method=="POST"):
            form=CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user=form.cleaned_data.get('username')
                messages.success(request, user+"'s account created successfully")#send a flash mesaage
                return redirect('login')

        context={'form':form}
        return render(request,'accounts/register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if(request.method=="POST"):
            username=request.POST.get('username')
            password=request.POST.get('password')

            user=authenticate(request,username=username,password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, "Username or password is incorrect")

        context={}
        return render(request,'accounts/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

#Adding decorator above home page view, if the user is not logged in then redirect him to 'login' url
@login_required(login_url='login')
def home(request):
    customers=Customer.objects.all()
    orders=Order.objects.all()
    total_customers=customers.count()
    total_orders=orders.count()
    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()

    context={'orders':orders,'customers':customers,'total_customers':total_customers,'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return  render(request,'accounts/dashboard.html',context)#this context data will be passed to dashboard.html

@login_required(login_url='login')
def customer(request,custId):
    customer=Customer.objects.get(id=custId)
    orders=customer.order_set.all() #get all the child object(of type order) of customer
    order_cnt=orders.count()

    myFilter=OrderFilter(request.GET, queryset=orders)#perform query on orders data
    orders=myFilter.qs #reset the orders variable to the filtered_orders

    context={'customer':customer,'orders':orders,'order_cnt':order_cnt,'myFilter':myFilter}
    return render(request,'accounts/customers.html',context)

@login_required(login_url='login')
def products(request):
    products=Product.objects.all()
    return render(request,'accounts/products.html', {'products':products})
    # {'products_name':products} we can call the value products_name having value products in products.html template

@login_required(login_url='login')
def createOrder(request,custId):
    OrderFormSet=inlineformset_factory(Customer, Order, fields=('product','status'), extra=5)#(parent modelobject, child model object, fields you want in form
    customer=Customer.objects.get(id=custId)
    formset= OrderFormSet(queryset=Order.objects.none(), instance=customer)#for which customer we want this form
    # form=OrderForm(initial={'customer':customer})#fill the 'customer' attribute of form with customer
    if request.method=='POST':
        # form=OrderForm(request.POST)#set the data revieved from htmlform to variable form
        formset=OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save() #save data
            return redirect('/') #redirect to home pagr
        # print(request.POST)
    context={'formset':formset}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
def updateOrder(request, orderId):
    order=Order.objects.get(id=orderId)
    form=OrderForm(instance=order)#set the order in form, it will already fill the form with order data
    if request.method=='POST':
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
def deleteOrder(request,orderId):
    order = Order.objects.get(id=orderId)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context={'item':order}
    return render(request,'accounts/delete_order.html',context)