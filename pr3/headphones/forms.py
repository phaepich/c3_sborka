from django import forms
from .models import Headphones, OrderItem


class HeadphonesForm(forms.ModelForm):
    class Meta:
        model = Headphones
        fields = '__all__'


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['headphones', 'quantity']
