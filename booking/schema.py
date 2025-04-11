import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from booking.models import Vehicle, Booking, Review
from employees.models import Profile

User = get_user_model()

class BookingType(DjangoObjectType):
    class Meta:
        model = Booking
        fields = ['id','vehicle','price','from_place', 'to_place', 'start_time','end_time', 'status']

class VehicleType(DjangoObjectType):
    class Meta:
        model = Vehicle
        fields = ['id', 'vehicle', 'brand', 'year', 'capicity', 'location', 'owner']
    
class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = ['id','user']

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

        
class Query(graphene.ObjectType):
    all_booking = graphene.List(BookingType)
    all_vehicle = graphene.List(VehicleType)
    all_profile = graphene.List(ProfileType)
    
    booking = graphene.Field(BookingType, id = graphene.String())
    vehicle = graphene.Field(VehicleType, id = graphene.Int())

    
    def resolve_all_booking(root, info):
        return Booking.objects.all()
    
    def resolve_booking(root, info, id):
        return Booking.objects.get(id = id)
    
    def resolve_all_vehicle(root, info):
        return Vehicle.objects.all()
    
    def resolve_vehicle(root, info, id):
        return Vehicle.objects.get(id = id)
    
    def resolve_all_profile(root, info):
        return Profile.objects.all()
    
    def resolve_all_user(root,info):
        return User.objects.all()

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


        
class Mutation(graphene.ObjectType):
    create_booking = BookingCreate.Field()
    update_booking = BookingUpdate.Field()

    create_vehicle = VehicleCreate.Field()
    update_vehicle = VehicleUpdate.Field()

    
schema = graphene.Schema(query = Query, mutation = Mutation)