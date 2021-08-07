from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.

def home(request):
    customers=Customer.objects.all()
    orders=Order.objects.all()
    total_customers=customers.count()
    total_orders=orders.count()
    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()

    context={'orders':orders,'customers':customers,'total_customers':total_customers,'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return  render(request,'accounts/dashboard.html',context)#this context data will be passed to dashboard.html

def customer(request,custId):
    customer=Customer.objects.get(id=custId)
    orders=customer.order_set.all() #get all the child object(of type order) of customer
    order_cnt=orders.count()
    context={'customer':customer,'orders':orders,'order_cnt':order_cnt}
    return render(request,'accounts/customers.html',context)

def products(request):
    products=Product.objects.all()
    return render(request,'accounts/products.html', {'products':products})
    # {'products_name':products} we can call the value products_name having value products in products.html template