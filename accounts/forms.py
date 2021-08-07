from django.forms import ModelForm
from .models import Order

class OrderForm(ModelForm):
    class Meta:
        model=Order
        fields='__all__' #take all the attributes of Order class present in models.py i.e ["customer","product","date_created","status"]