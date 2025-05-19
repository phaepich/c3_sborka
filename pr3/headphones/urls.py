from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.product_list,
        name='product_list'),
    path(
        'product/<int:pk>/',
        views.product_detail,
        name='product_detail'),
    path(
        'about/',
        views.about,
        name='about'),
    path(
        'cart/',
        views.cart_view,
        name='cart_view'),
    path(
        'cart/add/<int:pk>/',
        views.add_to_cart,
        name='add_to_cart'),
    path(
        'cart/remove/<int:item_id>/',
        views.remove_from_cart,
        name='remove_from_cart'),
    path(
        'product/<int:pk>/edit/',
        views.warehouseman_edit,
        name='warehouseman_edit'),
    path(
        'make_order/',
        views.make_order,
        name='make_order'),
]
