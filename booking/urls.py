from django.urls import path
from graphene_django.views import GraphQLView

from booking.schema import schema
from . import views

urlpatterns = [
    path('graphs/', GraphQLView.as_view(graphiql = True, schema = schema)),
    path("",views.BookingListView.as_view(), name = 'booking_list_url'),
    path("create/",views.BookingCreateView.as_view(), name = 'booking_create_url'),
    path("<booking_number>/",views.BookingDetailView.as_view(), name = 'booking_detail_url'),
    path("updated/<booking_number>/",views.BookingUpdateView.as_view(), name = 'booking_update_url'),
    path('delete/<booking_number>/', views.BookingDeleteView.as_view(), name = 'booking_delete_url'),
    path("vehicle/create/", views.VehicleCreateView.as_view(), name = 'vehicle_create_url'),
    path('vehicle/update/<vehicle_number>/', views.VehicleUpdateView.as_view(), name = 'vehicle_update_url'),
    path('review/<user_pk>/', views.ReviewCreateView.as_view(), name = 'review_url')
]