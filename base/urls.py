from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from .views import updateUserProfile, GetUserProfileView, getUsers


urlpatterns = [
    path('',views.getRoutes,name="getRoutes"),
    path('users/register/',views.registerUser,name='register'),
    path('users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('products/',views.getProducts,name="getProducts"),
    path('users/profile/',views.getUserProfiles,name="getUserProfiles"),
    path('products/<str:pk>',views.getProduct,name="getProduct"),
    # path('profile/update', views.updateUserProfile, name="user-profile-update"),
    path('users/',views.getUsers,name="getUsers"),


    path('add/', views.addorderItems, name='orders-add'),
    # path(' ',views.getOrders,name="allorders"),
    # path('orders/<str:pk>/', views.getOrderById, name='myorders'), 
    path('myorders/',views.getMyOrders,name="myorders"),
    path('<str:pk>/', views.getOrderById, name='user-order'),
    path('<str:pk>/pay/', views.updateOrdertoPaid, name='pay'),
    path('<str:pk>/deliver/',views.updateOrderToDelivered,name="delivered"),

    # path('update/<str:pk>/', views.updateUserProfile, name='update-user-profile'),
    path('profile/update/',views.updateUserProfile,name="user_profile_update"),
    path('user', GetUserProfileView.as_view()),
    path('users', views.getUsers, name="users"),
  
]
