"""
URL configuration for community project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path
from booking.views import BookingListView
from employees.views import RegisterUser

urlpatterns = [
    path("", BookingListView.as_view(), name = 'booking_list_url'),
    path('register/',RegisterUser.as_view(),name='register'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('admin/', admin.site.urls),
    path('employees/',include('employees.urls')),
    path('booking/',include('booking.urls')),
    path('orders/',include('orders.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('api/', include('api.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    

