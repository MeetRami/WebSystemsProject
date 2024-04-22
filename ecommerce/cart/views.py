from django.shortcuts import render, redirect
from .models import Product, CartItem
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


@login_required
def product_list(request):
    products = Product.objects.all()
    cart_items = CartItem.objects.filter(user=request.user)
    cart_products = [item.product for item in cart_items]
    for product in products:
        product.InCart = product in cart_products
    return render(request, 'index.html', {'products': products, 'username': request.user.username})


def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user.id)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    totalItems = sum(item.quantity for item in cart_items)
    username = request.user.username if request.user.is_authenticated else None
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'totalItems': totalItems, 'username': username})

def add_to_cart(request, product_id):
	product = Product.objects.get(id=product_id)
	cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
	cart_item.quantity = 1
	cart_item.save()
	return redirect('cart:view_cart')

def remove_from_cart(request, item_id):
	cart_item = CartItem.objects.get(id=item_id)
	cart_item.delete()
	return redirect('cart:view_cart')

def checkout(request):
	prev_cart_items = CartItem.objects.filter(user=request.user.id)
	cart_items = CartItem.objects.filter(user=request.user.id)
	total_price = sum(item.product.price * item.quantity for item in cart_items)
	for item in cart_items:
		cart_item = CartItem.objects.get(id=item.id)
		product = Product.objects.get(id=cart_item.product_id)
		product.isSold=True
		product.save()
		cart_item.delete()
	totalItems = 0
	return render(request, 'checkout.html', {'cart_items': prev_cart_items, 'total_price': total_price, 'totalItems':totalItems})

def home(request):
	return HttpResponse('Hello, World!')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('cart:product_list')
        else:
            error_message = "Invalid username or password. Please try again."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cart:product_list')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('cart:login_view')
