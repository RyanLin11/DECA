from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/edit/', views.update_profile, name='edit_profile'),
    path('', views.index, name='index'),
]