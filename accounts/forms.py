from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import  forms

from .models import Order

class OrderForm(ModelForm):
    class Meta:
        model=Order
        fields='__all__' #take all the attributes of Order class present in models.py i.e ["customer","product","date_created","status"]

# CreateUserForm class will inherit the prebuilt class 'UserCreationFrom'
class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']