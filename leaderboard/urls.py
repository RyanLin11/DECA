from django.urls import path
from django.urls import include
from . import views

#app_name = 'leaderboard'

urlpatterns = [
    path('', views.index, name='leaderboard'),
]