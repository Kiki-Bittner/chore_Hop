from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name ='home'),
    path('user_dash', views.user_dash),
    path('driver_dash', views.driver_dash)
]
