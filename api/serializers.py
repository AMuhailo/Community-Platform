from rest_framework import serializers
from booking.models import Booking, Vehicle, Review
from orders.models import Order
from employees.models import Moderator, Member

class VehicleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id','vehicle','brand','year','capicity','location','owner']
        
class BookingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id','vehicle','price','from_place','to_place','start_time','end_time','status']
        
class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','booking','price','capacity','owner','user','owner']
        

class ModeratorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Moderator
        fields = ['id','user','admin']

class MemberSerializers(serializers.ModelSerializer):
    review = serializers.IntegerField(read_only = True)
    class Meta:
        model = Member
        fields = ['id','user','category','review']