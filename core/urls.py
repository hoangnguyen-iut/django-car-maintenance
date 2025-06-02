from django.urls import path
from . import views

urlpatterns = [
    # URL cho trang chủ: rỗng nghĩa là "/"
    path('', views.home, name='home'),
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/add/', views.add_vehicle, name='add_vehicle'),
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('garages/', views.garage_list, name='garage_list'),
]