from django.contrib import admin
from .models import Headphones, FormFactor, Cart, CartItem
admin.site.register(Headphones)
admin.site.register(FormFactor)
admin.site.register(Cart)
admin.site.register(CartItem)
