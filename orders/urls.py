from django.urls import path
from . import views

urlpatterns = [
    path('',views.OrderListView.as_view(), name = 'order_url'),
    path('<booking_id>/orders/',views.OrderCreateView.as_view(), name = 'order_create_url'),
    path('<order_id>/cancel/',views.OrderDeleteView.as_view(), name = 'order_cancel_url')
]
