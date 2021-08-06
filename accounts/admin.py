from django.contrib import admin

# Register your models here.

from .models import *

#to show Customer table to django admin page
admin.site.register(Customers)
admin.site.register(Product)
admin.site.register(Order)