from django.urls import path
from . import views

app_name = 'NFTWebsite'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    # Add more URL patterns as needed
]
