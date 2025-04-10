from django.urls import include, path    
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from . import views 

router = routers.DefaultRouter()
router.register(r'vehicle', views.VehicleAPIViewset)
router.register(r'booking', views.BookingAPIViewset)
router.register(r'order', views.OrderAPIViewset)
router.register(r'moderator', views.ModerAPIViewset)
router.register(r'member', views.MemberAPIViewwet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),   
]