from django.urls import path
from . import views

urlpatterns = [
    path("",views.BookingListView.as_view(), name = 'booking_list_url'),
    path("<booking_number>/",views.BookingDetailView.as_view(), name = 'booking_detail_url'),
    path("create//",views.BookingCreateView.as_view(), name = 'booking_create_url'),
    path("updated/<booking_number>/",views.BookingUpdateView.as_view(), name = 'booking_update_url'),
]

