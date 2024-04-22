from django.shortcuts import render, redirect
from .models import Product, CartItem
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login


def add_to_cart(request, product_id):
    # Retrieve the product object
    product = get_object_or_404(Product, id=product_id)
    
    # Check if the user is authenticated
    if isinstance(request.user, AnonymousUser):
        # If the user is not authenticated, handle accordingly
        return JsonResponse({'message': 'Please log in to add items to your cart'}, status=401)
    
    # If the user is authenticated, proceed with adding the item to the cart
    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
    cart_item.quantity = 1
    cart_item.save()
    
    # Return a JsonResponse indicating success
    return JsonResponse({'message': 'Item added to cart successfully'})

def product_list(request):
	products = Product.objects.all()
	cartItems = CartItem.objects.all()
	totalItems = 0
	totalItems += sum(item.quantity for item in cartItems)
	return render(request, 'index.html', {'products': products, 'totalItems':totalItems})

def view_cart(request):
	cart_items = CartItem.objects.filter(user=request.user.id)
	total_price = sum(item.product.price * item.quantity for item in cart_items)
	totalItems = 0
	totalItems += sum(item.quantity for item in cart_items)
	return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'totalItems':totalItems})

def add_to_cart(request, product_id):
	product = Product.objects.get(id=product_id)
	cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
	cart_item.quantity = 1
	cart_item.save()
	return JsonResponse({'message': 'Item added to cart'})

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

# def remove_one_from_cart(request, item_id):
# 	cart_item = CartItem.objects.get(id=item_id)
# 	if cart_item.quantity==1:
# 		cart_item.delete()
# 	else:
# 		cart_item.quantity -= 1
# 		cart_item.save()
# 	return redirect('cart:view_cart')

def home(request):
	return HttpResponse('Hello, World!')

def login_view(request):
    if request.method == 'POST':
        # Extract username and password from the POST data
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        # If user is authenticated, log them in and redirect to a protected page
        if user is not None:
            login(request, user)
            # Redirect to a success page, or any other desired page
            return redirect('home')  # Replace 'home' with the name of your homepage URL
        else:
            # If authentication fails, display an error message
            error_message = "Invalid username or password. Please try again."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        # If request method is GET, render the login page
        return render(request, 'login.html')