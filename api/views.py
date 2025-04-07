from rest_framework import generics 
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count
from api.serializers import BookingSerializers, OrderSerializers, VehicleSerializers
from booking.models import Vehicle, Booking, Review
from orders.models import Order


# Create your views here.

class VehicleAPIViewset(ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializers
    def list(self, request, *args, **kwargs):
        cars = Vehicle.objects.filter(vehicle = 'car')
        car_data = self.get_serializer(cars, many = True).data
        bus = Vehicle.objects.filter(vehicle = 'bus')
        bus_data = self.get_serializer(bus, many = True).data
        return Response({'cars_count':len(car_data),
                         'bus_count':len(bus_data),
                         "transpost":{'car':car_data,
                                      'bus':bus_data}})
    
    def retrieve(self, request, *args, **kwargs):
        vehicle = self.get_object()
        vehicle_srz = self.get_serializer(vehicle).data
        return Response({'transport': vehicle_srz})

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({'transport': response.data})


class BookingAPIViewset(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializers
    def list(self, request, *args, **kwargs):
        complete_booking = Booking.objects.filter(status = 'complete')
        cancelled_booking = Booking.objects.filter(status = 'cancelled')
        pending_booking = Booking.objects.filter(status = 'pending')
        complete_data = self.get_serializer(complete_booking, many = True).data
        cancelled_data = self.get_serializer(cancelled_booking, many = True).data
        pending_data = self.get_serializer(pending_booking, many = True).data
        return Response({"booking_data":[
                                {
                                    'complete':complete_data, 
                                    'cencelled':cancelled_data, 
                                    'pending':pending_data
                                }
                            ]
                        })
    
    def retrieve(self, request, *args, **kwargs):
        booking = self.get_object()
        booking_data = self.get_serializer(booking).data
        orders = booking.order_booking.all()
        order_data = OrderSerializers(orders, many = True).data
        booking_data['order'] = order_data
        return Response({f"booking_{str(booking.id)[:4]}":[
                                {
                                    f"{booking.status}":booking_data,
                                }
                            ]
                        })
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs).data
        return Response({f"booking_{str(response.id)[:4]}":[
                                {
                                    f"{response.status}":response
                                }
                            ]
                        })
        
class OrderAPIViewset(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    
    def list(self, request, *args, **kwargs):
        orders = self.queryset
        order_data = self.get_serializer(orders, many = True).data
        return Response({"orders":order_data})
    
    def retrieve(self, request, *args, **kwargs):
        order = self.get_object()
        booking = order.booking
        order_data = self.get_serializer(order, many = False).data
        booking_data = BookingSerializers(booking, many = False).data        
        return Response({f"order_{str(order.id)[:4]}":[
                                {
                                    'data':order_data,
                                    'booking':booking_data
                                }
                            ]
                        })