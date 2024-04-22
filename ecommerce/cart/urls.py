from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
	path('', views.product_list, name='product_list'),
	#path('', views.home, name='home'),
	path('cart/', views.view_cart, name='view_cart'),
	path('checkout/', views.checkout, name='checkout'),
	path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
	path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
	#path('remove_one/<int:item_id>/', views.remove_one_from_cart, name='remove_one_from_cart'),
	path('login/', views.login_view, name='login'),
]
