import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from graphene_django.fields import DjangoListField
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.utils import timezone
from graphql import GraphQLError
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
    
    user = graphene.Field(UserType)
    
    def resolve_booking(root, info, id):
        return Booking.objects.get(id = id)
    
    def resolve_vehicle(root, info, id):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception('Unregistered!')
        return Vehicle.objects.get(id = id)
    
    def resolve_order(root, info, id):
        return Order.objects.get(id = id)

    def resolve_member(root, info, username):
        return Member.objects.get(user__user__username = username)

    def resolve_user(root, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        return user
class ObtainToken(graphql_jwt.ObtainJSONWebToken):
    @classmethod
    def resolve(cls,root, info, **kwargs):
        return super().resolve(root,info,**kwargs)    

class RegisterUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required = True)
        email = graphene.String(required = True)
        password = graphene.String(required = True)

    success = graphene.Boolean()
    user_id = graphene.ID()
    message = graphene.String()
    def mutate(self, info , username, email, password):
        if User.objects.filter(username = username).exists():
            raise GraphQLError("Username already taken")
        if User.objects.filter(email = email).exists():
            raise GraphQLError("Email already taken")
        validate_password(password)
        user = User.objects.create_user(username = username, email = email, password=password)
        return RegisterUser(user_id= user.id, success = True, message = "You have authorized.")

class UpdateUser(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required = True)
        last_name = graphene.String(required = True)
    
    success = graphene.Boolean()
    message = graphene.String()
    user_id = graphene.ID()
    
    def mutate(self, info, first_name, last_name):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        user = User.objects.get(username = user.username)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return UpdateUser(user_id = user.id, success = True, message = 'You have successfully updated your data!')
    
    
class VehicleCreate(graphene.Mutation):
    class Arguments:
        vehicle = graphene.String()
        brand = graphene.String()
        year = graphene.Int()
        capicity = graphene.Int()
        location = graphene.String()
        owner = graphene.ID()
        
    vehicle = graphene.Field(VehicleType)
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(self, info, vehicle, brand, year, capicity, location, owner):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception(f"You are not authorized!")
        
        if not user.profile.member_user.category == "DR":
            raise Exception("You are not a driver.")
        vehicle = Vehicle.objects.create(
            vehicle = vehicle,
            brand = brand,
            year = year,
            capicity = capicity,
            location = location,
            owner_id = owner
        )
        return VehicleCreate(vehicle = vehicle, success = True, message = "Vehicle success created!")


class VehicleUpdate(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)
        capicity = graphene.Int(required = True)
        location = graphene.String(required = True)
        
    vehicle = graphene.Field(VehicleType)
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(self, info, id, capicity, location):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception(f"You are not authorized!")
        
        if not user.profile.member_user.category == "DR":
            raise Exception("You are not a driver.")
        vehicle = Vehicle.objects.get(id = id)
        vehicle.capicity = capicity
        vehicle.location = location
        vehicle.save()
        return VehicleUpdate(vehicle = vehicle, success = True, message = "Vehicle success updated!")


class VehicleDelete(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)
        
    vehicle = graphene.Field(VehicleType)
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(self, info, id):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception(f"You are not authorized!")
        if not user.profile.member_user.category == "DR":
            raise Exception("You are not a driver.")
        
        vehicle = Vehicle.objects.get(id = id)
        vehicle.delete()
        return VehicleUpdate(vehicle = vehicle, success = True, message = "Vehicle success deleted!")


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
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(self, info, vehicle, price, from_place, to_place, start_time, end_time):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception(f"You are not authorized!")
        booking = Booking.objects.create(vehicle_id = vehicle, 
                               price = price, 
                               from_place = from_place,
                               to_place = to_place,
                               start_time = start_time, 
                               end_time = end_time,
                               status = 'complete')
        return BookingCreate(booking = booking, success = True, message = "Booking success created!")

    
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
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(self, info, id, price, from_place, to_place):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception(f"You are not authorized!")
        booking = Booking.objects.get(id=id)
        booking.price = price
        booking.from_place = from_place
        booking.to_place = to_place
        booking.save()
        return BookingUpdate(booking = booking, success = True, message = "Booking success updated!")

class BookingDelete(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)
        
    booking = graphene.Field(BookingType)
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(self, info, id):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception(f"You are not authorized!")
        booking = Booking.objects.get(id=id)
        booking.delete()
        return BookingUpdate(booking = booking, success = True, message = "Booking success deleted!")


class OrderCreate(graphene.Mutation):
    class Arguments:
        booking = graphene.ID()
        capacity = graphene.Int()
        user = graphene.ID()
    
    orders = graphene.Field(OrderType)
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(self, info , booking, capacity):
        user = info.context.user
        booking = Booking.objects.get(id = booking)
        try:
            if not user.is_authenticated:
                raise Exception(f"You are not authorized!")
            
            
            if capacity > booking.vehicle.capicity:
                raise Exception(f"The number of places cannot be greater than {booking.vehicle.capicity}")
            
            orders = Order.objects.create(booking = booking,
                                        price = booking.price,
                                        capacity = capacity, 
                                        owner = booking.vehicle.owner.user,
                                        user = user,
                                        date = timezone.now().date())    
            return OrderCreate(orders = orders, success = True, message = 'The order has been created.')
                
        except:
            raise Exception(f"An unexpected error occurred!")
    
class OrderUpdate(graphene.Mutation):
    class Arguments:
        id = graphene.String(required = True)
        booking = graphene.ID(required = True)
        price = graphene.String(required = True)
        capacity = graphene.Int(required = True)
        date = graphene.Date(required = True)
        
    orders = graphene.Field(OrderType)
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(self, info , id, booking, capacity, date):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception(f"You are not authorized!")
        
        orders = Order.objects.get(id = id)
        orders.booking = booking
        orders.capacity = capacity
        orders.date = date
        orders.save()
        
        return OrderUpdate(orders = orders, success = True, message = 'The order has been updated.')
    
class OrderDelete(graphene.Mutation):
    class Arguments:
        id = graphene.String(required = True)
        
    orders = graphene.Field(OrderType)
    
    def mutate(self, info , id):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception(f"You are not authorized!")
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
    
    token_auth = ObtainToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()
    
    
    update_user = UpdateUser.Field()
    register = RegisterUser.Field()
    
    
schema = graphene.Schema(query = Query, mutation = Mutation)
