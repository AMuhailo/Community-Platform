from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.RegisterUser.as_view(), name='register'),
    path('moder/create/',views.ModeratorCreateView.as_view(), name = 'moder_create')
]
