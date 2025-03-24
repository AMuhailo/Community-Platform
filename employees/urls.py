from django.urls import path
from . import views
urlpatterns = [
    path('moder/', views.ModeratorListView.as_view(), name = 'moder_url'),
    path('moder/create/',views.ModeratorCreateView.as_view(), name = 'moder_create_url'),
    path('moder/update/<username>/<user_id>/', views.ModeratorUpdateView.as_view(), name = 'moder_update_url'),
    
]

memberpatterns = [
    path('member/', views.MemberListView.as_view(), name = 'member_url')
]

urlpatterns += memberpatterns