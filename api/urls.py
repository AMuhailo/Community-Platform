from django.urls import include, path    
from rest_framework import routers
from . import views 

router = routers.DefaultRouter()
router.register(r'vehicle', views.VehicleAPIViewset)
router.register(r'booking', views.BookingAPIViewset)
router.register(r'order', views.OrderAPIViewset)
router.register(r'moderator', views.ModerAPIViewset)
router.register(r'member', views.MemberAPIViewwet)
urlpatterns = [
    path('', include(router.urls)),
    path('<vehicle_id>/', include(router.urls)),
    path('<booking_id>/', include(router.urls)),
    path('<order_id>/', include(router.urls)),
    path('<moderator_id>/', include(router.urls)),
    path('<member_id>/', include(router.urls)),
]
