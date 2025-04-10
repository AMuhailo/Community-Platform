from rest_framework import generics 
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from django.db.models import Count
from api.permissions import IsMemberPermission
from api.serializers import BookingSerializers, OrderSerializers, VehicleSerializers, ModeratorSerializers, MemberSerializers
from booking.models import Vehicle, Booking
from employees.models import Member, Moderator
from orders.models import Order


# Create your views here.
class PaginationAPIAll(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'pages'
    max_page_size = 10


class VehicleAPIViewset(ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializers
    permission_classes = [IsAuthenticated]
    pagination_class = PaginationAPIAll
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
        return Response({'transport':{
                                'id':vehicle.id,
                                'vehicle':vehicle.vehicle,
                                f'{vehicle.vehicle}_data':{
                                    'brand':vehicle.brand,
                                    'year':vehicle.year,
                                    'capacity':vehicle.capicity,
                                    'location':vehicle.location
                                },
                                'owner':{
                                    'first_name':vehicle.owner.user.first_name,
                                    'last_name':vehicle.owner.user.last_name,
                                }
                            }
                         })

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs).data
        return Response({'transport': response})


class BookingAPIViewset(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PaginationAPIAll

    def list(self, request, *args, **kwargs):
        complete_booking = Booking.objects.filter(status = 'complete')
        cancelled_booking = Booking.objects.filter(status = 'cancelled')
        pending_booking = Booking.objects.filter(status = 'pending')
        complete_data = self.get_serializer(complete_booking, many = True).data
        cancelled_data = self.get_serializer(cancelled_booking, many = True).data
        pending_data = self.get_serializer(pending_booking, many = True).data
        return Response({"booking_data":[
                                    {
                                    'complete_count':len(complete_data),
                                    'cancelle_count':len(cancelled_data),
                                    'pending_count':len(pending_data)
                                },
                                {
                                    'complete':complete_data, 
                                    'cencelled':cancelled_data, 
                                    'pending':pending_data
                                }
                            ]
                        })
    
    def retrieve(self, request, *args, **kwargs):
        booking = self.get_object()
        orders = booking.order_booking.all()
        orders_data = OrderSerializers(orders, many = True).data
        return Response({f"booking_{str(booking.id)[:4]}":
                                {
                                    f"{booking.status}":{
                                        'id':booking.id,
                                        "vehicle":booking.vehicle.vehicle,
                                        "price":booking.price,
                                        'trips':{
                                            'from':booking.from_place,
                                            'to':booking.to_place
                                        },
                                        'start_time':[
                                                {
                                                    "date":booking.start_time.date(), 
                                                    "time":booking.start_time.time()
                                                }
                                            ],
                                        'end_time':[
                                                {
                                                    "date":booking.end_time.date(), 
                                                    "time":booking.end_time.time()
                                                }
                                            ],
                                        'orders':orders_data
                                    },
                                }
                        })
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs).data
        return Response({f"booking0":[{
                                    f"status":response
                                }]
                        })
        
class OrderAPIViewset(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    permission_classes = [IsAuthenticated]
    pagination_class = PaginationAPIAll
    def list(self, request, *args, **kwargs):
        orders = self.queryset
        order_data = self.get_serializer(orders, many = True).data
        return Response({"count":len(order_data),"orders":order_data})
    
    def retrieve(self, request, *args, **kwargs):
        order = self.get_object()
        booking = order.booking
        return Response({f"order_{str(order.id)[:4]}":{
                                    'order_data':{
                                            "id":order.id,
                                            "price":order.price,
                                            "capacity": order.capacity,
                                            "owner":{
                                                "first_name":order.owner.first_name,
                                                "last_name":order.owner.last_name,
                                            },
                                            "user":{
                                                "first_name":order.user.first_name,
                                                "last_name":order.user.last_name,
                                            },
                                        },
                                        f"booking_{str(booking.id)[:4]}":
                                            {
                                                f"{booking.status}":{
                                                    'id':booking.id,
                                                    "vehicle":booking.vehicle.vehicle,
                                                    "price":booking.price,
                                                    'trips':{
                                                        'from':booking.from_place,
                                                        'to':booking.to_place
                                                    },
                                                    'start_time':[
                                                            {
                                                                "date":booking.start_time.date(), 
                                                                "time":booking.start_time.time()
                                                            }
                                                        ],
                                                    'end_time':[
                                                            {
                                                                "date":booking.end_time.date(), 
                                                                "time":booking.end_time.time()
                                                            }
                                                        ],
                                                },
                                            }    
                                    }
                                })
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs).data
        return Response({f"booking0":[{
                                    f"status":response
                                }]
                        })
        
        
class ModerAPIViewset(ModelViewSet):
    queryset = Moderator.objects.all()
    serializer_class = ModeratorSerializers
    permission_classes = [IsAdminUser]
    pagination_class = PaginationAPIAll
    def list(self, request, *args, **kwargs):
        moders = self.queryset
        moder_data = self.get_serializer(moders, many = True).data
        return Response({'moders':moder_data})
    
    def retrieve(self, request, *args, **kwargs):
        moder = self.get_object()
        return Response({f'moder_{moder.id}':{
                                "id":moder.id,
                                'user':{"first_name":moder.user.user.first_name,
                                        "last_name":moder.user.user.last_name
                                       }
                            }
                         })
        
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs).data
        return Response({f"booking0":[{
                                    f"status":response
                                }]
                        })

class MemberAPIViewwet(ModelViewSet):
    serializer_class = MemberSerializers
    queryset = Member.objects.annotate(review=Count('user__user__review_received', distinct=True))
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PaginationAPIAll
    def list(self, request, *args, **kwargs):
        members = self.queryset
        
        member_mb = members.filter(category = 'MB')
        member_dr = members.filter(category = 'DR')
        member_data = MemberSerializers(members, many = True).data
        return Response({"category":{
                                "driver":len(member_dr),
                                "member":len(member_mb),
                            },
                        'member':member_data,
                        })
        
        
    def retrieve(self, request, *args, **kwargs):
        member = self.get_object()
        vehicle = member.user.owner_vehicle.all()
        if vehicle:
            vehicle = VehicleSerializers(vehicle, many = True).data
        else:
            vehicle = None
        return Response({f"member_{member.id}":{
                                'first_name':member.user.user.first_name,
                                'last_name':member.user.user.last_name,
                                'category':member.category,
                                'age':member.user.age,
                                'reviews':len(member.user.user.review_received.all()),
                                'vehicle':vehicle,
                            }   
                        })