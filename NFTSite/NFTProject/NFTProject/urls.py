from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='login/', permanent=False)),  # Redirect to login page
    path('login/', include('NFTWebsite.urls')),  # Include your app's URLs
    path('dashboard/', include('NFTWebsite.urls')),  # Include your app's URLs
]
