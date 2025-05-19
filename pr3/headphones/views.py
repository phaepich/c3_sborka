from django import forms
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from .models import Headphones, FormFactor, Cart, CartItem


def is_manager(user):
    return user.groups.filter(
        name="Менеджер по продажам").exists() or user.is_superuser


def is_warehouseman(user):
    return user.groups.filter(name="Товаровед").exists() or user.is_superuser


def is_normal_user(user):
    return (
        user.is_authenticated
        and not user.groups.filter(name="Товаровед").exists()
        and not user.is_superuser
    )


def product_list(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'brand')
    allowed_sorts = ['brand', 'impedance', 'weight']
    if sort_by not in allowed_sorts:
        sort_by = 'brand'
    form_factor_id = request.GET.get('form_factor')
    products = Headphones.objects.all()
    if query:
        products = products.filter(
            brand__icontains=query) | products.filter(
            article__icontains=query)
    if form_factor_id:
        products = products.filter(form_factor_id=form_factor_id)
    products = products.order_by(sort_by)
    form_factors = FormFactor.objects.all()
    return render(
        request,
        'headphones/product_list.html',
        {
            'products': products,
            'form_factors': form_factors,
            'selected_sort': sort_by,
            'selected_form_factor': int(form_factor_id) if form_factor_id
            else None,
            'query': query,
            'is_customer': request.user.is_authenticated and
            not is_warehouseman(
                request.user) and not request.user.is_superuser})


def product_detail(request, pk):
    product = get_object_or_404(Headphones, pk=pk)
    is_warehouseman_flag = False
    if request.user.is_authenticated and (request.user.groups.filter(
            name="Товаровед").exists() or request.user.is_superuser):
        is_warehouseman_flag = True
    is_customer = request.user.is_authenticated and not is_warehouseman(
        request.user) and not request.user.is_superuser
    return render(request, 'headphones/product_detail.html', {
        'product': product,
        'is_warehouseman': is_warehouseman_flag,
        'is_customer': is_customer,
    })


def about(request):
    return render(request, 'headphones/about.html')


@login_required
def cart_view(request):
    if not is_normal_user(request.user) and not is_manager(request.user):
        return HttpResponseForbidden("Вам запрещено пользоваться корзиной")
    cart, _ = Cart.objects.get_or_create(user=request.user)
    if request.method == "POST":
        changed = False
        for item in cart.items.all():
            qty = request.POST.get(f"qty_{item.id}")
            if qty is not None:
                try:
                    qty = int(qty)
                    if qty > 0:
                        item.quantity = qty
                        item.save()
                        changed = True
                    else:
                        item.delete()
                        changed = True
                except ValueError:
                    continue
        if changed:
            return redirect('cart_view')
    is_manager_flag = is_manager(request.user)
    return render(request, "headphones/cart.html",
                  {"cart": cart, "is_manager": is_manager_flag})


@login_required
def add_to_cart(request, pk):
    if not is_normal_user(request.user) and not is_manager(request.user):
        return HttpResponseForbidden("Вам запрещено пользоваться корзиной")
    product = get_object_or_404(Headphones, pk=pk)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
    else:
        item.quantity = 1
    item.save()
    return redirect('cart_view')


@login_required
def remove_from_cart(request, item_id):
    if not is_normal_user(request.user) and not is_manager(request.user):
        return HttpResponseForbidden("Вам запрещено пользоваться корзиной")
    item = get_object_or_404(CartItem, id=item_id)
    if item.cart.user == request.user:
        item.delete()
    return redirect('cart_view')


class HeadphonesForm(forms.ModelForm):
    class Meta:
        model = Headphones
        fields = [
            'article',
            'brand',
            'wireless',
            'impedance',
            'weight',
            'color',
            'form_factor',
            'price',
            'wholesale_price_small',
            'wholesale_qty_small',
            'wholesale_price_big',
            'wholesale_qty_big']


@user_passes_test(is_warehouseman)
def warehouseman_edit(request, pk):
    product = get_object_or_404(Headphones, pk=pk)
    if request.method == 'POST':
        form = HeadphonesForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = HeadphonesForm(instance=product)
    return render(request, 'headphones/warehouseman_edit.html',
                  {'form': form, 'product': product})


@user_passes_test(is_manager)
def make_order(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    order_sum = cart.total_price()
    if request.method == "POST" and items:
        items.delete()
        return render(request,
                      "headphones/order_success.html",
                      {"sum": order_sum})
    return render(request, "headphones/make_order.html", {"cart": cart})
