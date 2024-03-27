from django.urls import path
from . import views
    

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    
    path('', views.home, name="home"),
    path('group/<str:pk>/', views.group, name="group"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-group/', views.createGroup, name="create-group"),
    path('update-group/<str:pk>/', views.updateGroup, name="update-group"),
    path('delete-group/<str:pk>/', views.deleteGroup, name="delete-group"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('update-user/', views.updateUser, name="update-user"),
]