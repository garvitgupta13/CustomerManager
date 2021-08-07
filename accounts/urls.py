from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('products/',views.products,name="products"),
    path('customer/<str:custId>',views.customer,name="customer"),#instead of calling the link we name it as 'customer
    path('create_order/',views.createOrder, name="create_order"),
    path('update_order/<str:orderId>',views.updateOrder, name="update_order"),
    path('delete_order/<str:orderId>',views.deleteOrder, name="delete_order")
]