from django.urls import path
from . import views

urlpatterns = [
    # URL cho trang chủ: rỗng nghĩa là "/"
    path('', views.home, name='home'),
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/add/', views.add_vehicle, name='add_vehicle'),
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/add/', views.add_maintenance, name='add_maintenance'),
    path('garages/', views.garage_list, name='garage_list'),
    path('vehicles/<int:pk>/edit/', views.edit_vehicle, name='edit_vehicle'),
    path('vehicles/<int:pk>/delete/', views.delete_vehicle, name='delete_vehicle'),
    path('garage/<int:pk>/', views.garage_detail, name='garage_detail'),
]