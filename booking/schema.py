import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphene_django.fields import DjangoListField
from django.utils import timezone
from booking.models import Vehicle, Booking, Review
from employees.models import Profile, Moderator, Member
from orders.models import Order

User = get_user_model()

class BookingType(DjangoObjectType):
    class Meta:
        model = Booking
        fields = ['id','vehicle','price','from_place', 'to_place', 'start_time','end_time', 'status']

class VehicleType(DjangoObjectType):
    class Meta:
        model = Vehicle
        fields = ['id', 'vehicle', 'brand', 'year', 'capicity', 'location', 'owner']
    
class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ['id', 'booking','price','capacity', 'owner', 'user', 'date']
    
class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = ['id','user']

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name', 'email']

class MemberType(DjangoObjectType):
    class Meta:
        model = Member
        fields = ['user', 'category', 'created']


class ModersType(DjangoObjectType):
    class Meta:
        model = Member
        fields = ['id','user']

class Query(graphene.ObjectType):
    all_booking = DjangoListField(BookingType)
    all_vehicle = DjangoListField(VehicleType)
    all_orders = DjangoListField(OrderType)
    
    all_profile = DjangoListField(ProfileType)
    all_member = DjangoListField(MemberType)
    all_moder = DjangoListField(ModersType)
    
    booking = graphene.Field(BookingType, id = graphene.String())
    vehicle = graphene.Field(VehicleType, id = graphene.Int())
    orders = graphene.Field(OrderType, id = graphene.String())
    member = graphene.Field(MemberType, username = graphene.String())
    
    
    def resolve_booking(root, info, id):
        return Booking.objects.get(id = id)
    
    def resolve_vehicle(root, info, id):
        return Vehicle.objects.get(id = id)
    
    def resolve_order(root, info, id):
        return Order.objects.get(id = id)

    def resolve_member(root, info, username):
        return Member.objects.get(user__user__username = username)


class VehicleCreate(graphene.Mutation):
    class Arguments:
        vehicle = graphene.String()
        brand = graphene.String()
        year = graphene.Int()
        capicity = graphene.Int()
        location = graphene.String()
        owner = graphene.ID()
        
    vehicle = graphene.Field(VehicleType)
    
    def mutate(self, info, vehicle, brand, year, capicity, location, owner):
        vehicle = Vehicle.objects.create(
            vehicle = vehicle,
            brand = brand,
            year = year,
            capicity = capicity,
            location = location,
            owner_id = owner
        )
        return VehicleCreate(vehicle = vehicle)


class VehicleUpdate(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)
        capicity = graphene.Int(required = True)
        location = graphene.String(required = True)
        
    vehicle = graphene.Field(VehicleType)
    
    def mutate(self, info, id, capicity, location):
        vehicle = Vehicle.objects.get(id = id)
        vehicle.capicity = capicity
        vehicle.location = location
        vehicle.save()
        return VehicleUpdate(vehicle = vehicle)


class VehicleDelete(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)
        
    vehicle = graphene.Field(VehicleType)
    
    def mutate(self, info, id):
        vehicle = Vehicle.objects.get(id = id)
        vehicle.delete()
        return VehicleUpdate(vehicle = vehicle)


class BookingCreate(graphene.Mutation):
    class Arguments:
        vehicle = graphene.ID()
        price = graphene.String()
        from_place = graphene.String()
        to_place = graphene.String()
        start_time = graphene.DateTime()
        end_time = graphene.DateTime()
        status = graphene.String()
    
    booking = graphene.Field(BookingType)
    
    def mutate(self, info, vehicle, price, from_place, to_place, start_time, end_time, status):
        booking = Booking.objects.create(vehicle_id = vehicle, 
                               price = price, 
                               from_place = from_place,
                               to_place = to_place,
                               start_time = start_time, 
                               end_time = end_time,
                               status = status)
        return BookingCreate(booking = booking)

    
class BookingUpdate(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)
        price = graphene.String(required = True)
        from_place = graphene.String(required = True)
        to_place = graphene.String(required = True)
        start_time = graphene.DateTime(required = True)
        end_time = graphene.DateTime(required = True)
        status = graphene.String(required = True)
        
    booking = graphene.Field(BookingType)

    def mutate(self, info, id, price, from_place, to_place):
        booking = Booking.objects.get(id=id)
        booking.price = price
        booking.from_place = from_place
        booking.to_place = to_place
        booking.save()
        return BookingUpdate(booking = booking)

class BookingDelete(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)
        
    booking = graphene.Field(BookingType)

    def mutate(self, info, id):
        booking = Booking.objects.get(id=id)
        booking.delete()
        return BookingUpdate(booking = booking)


class OrderCreate(graphene.Mutation):
    class Arguments:
        booking = graphene.ID()
        capacity = graphene.Int()
        user = graphene.ID()
    
    orders = graphene.Field(OrderType)
    
    def mutate(self, info , booking, capacity, user):
        booking = Booking.objects.get(id = booking)
        orders = Order.objects.create(booking = booking,
                                    price = booking.price,
                                    capacity = capacity, 
                                    owner = booking.vehicle.owner.user,
                                    user_id = user,
                                    date = timezone.now().date())    
        return OrderCreate(orders = orders)
    
class OrderUpdate(graphene.Mutation):
    class Arguments:
        id = graphene.String(required = True)
        booking = graphene.ID(required = True)
        price = graphene.String(required = True)
        capacity = graphene.Int(required = True)
        owner = graphene.ID(required = True)
        user = graphene.ID(required = True)
        date = graphene.Date(required = True)
        
    orders = graphene.Field(OrderType)
    
    def mutate(self, info , id, booking, price, capacity, owner, user, date):
        orders = Order.objects.get(id = id)
        orders.booking = booking
        orders.price = price
        orders.capacity = capacity
        orders.owner = owner
        orders.user = user
        orders.date = date
        orders.save()
        
        return OrderUpdate(orders = orders)
    
class OrderDelete(graphene.Mutation):
    class Arguments:
        id = graphene.String(required = True)
        
    orders = graphene.Field(OrderType)
    
    def mutate(self, info , id):
        orders = Order.objects.get(id = id)
        orders.delete()
        return OrderUpdate(orders = orders)
    
    
class Mutation(graphene.ObjectType):
    create_booking = BookingCreate.Field()
    update_booking = BookingUpdate.Field()
    delete_booking = BookingDelete.Field()
    
    create_vehicle = VehicleCreate.Field()
    update_vehicle = VehicleUpdate.Field()
    delete_booking = VehicleDelete.Field()
    
    create_orders = OrderCreate.Field()
    update_orders = OrderUpdate.Field()
    delete_orders = OrderDelete.Field()
    
schema = graphene.Schema(query = Query, mutation = Mutation)
