from django.urls import path
from . import views
urlpatterns = [
    path('moder/', views.ModeratorListView.as_view(), name = 'moder_url'),
    path('moder/create/',views.ModeratorCreateView.as_view(), name = 'moder_create_url'),
    path('member/', views.MemberListView.as_view(), name = 'member_url'),
    path('profile/<username>/', views.ProfileUser.as_view(), name = 'profile_url'),
    path('moder/update/<username>/<user_id>/', views.ProfileUpdateView.as_view(), name = 'profile_update_url'),
    path('<member_id>/category/', views.CategoryUpdateView.as_view(), name = 'category_update_url'),
]