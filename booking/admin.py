from django.contrib import admin
from booking.models import Vehicle, Booking, Review

# Register your models here.


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['vehicle','brand','year','capicity','location','owner']
    list_filter = ['vehicle','year']
    list_editable = ['year','location','capicity']
    
admin.site.register(Booking)
admin.site.register(Review)