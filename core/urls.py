from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

urlpatterns = [
    # Chuyển hướng về /login thay vì /accounts/login
    path('', lambda request: redirect('/login/?next=/vehicles/'), name='home'),
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/add/', views.add_vehicle, name='add_vehicle'),
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/add/', views.add_maintenance, name='add_maintenance'),
    path('garages/', views.garage_list, name='garage_list'),
    path('vehicles/<int:pk>/edit/', views.edit_vehicle, name='edit_vehicle'),
    path('vehicles/<int:pk>/delete/', views.delete_vehicle, name='delete_vehicle'),
    path('garage/<int:pk>/', views.garage_detail, name='garage_detail'),
    path('maintenance/<int:pk>/edit/', views.edit_maintenance, name='edit_maintenance'),
    path('maintenance/<int:pk>/delete/', views.delete_maintenance, name='delete_maintenance'),
    path('garage/<int:garage_id>/appointment/', views.create_appointment, name='create_appointment'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('login/', auth_views.LoginView.as_view(
        template_name='core/login.html',
        next_page='/vehicles/'  # Thêm dấu / ở cuối
    ), name='login'),
    path('register/', views.register, name='register'),  # Thay đổi từ accounts/register/
    path('logout/', auth_views.LogoutView.as_view(
        next_page='/login/',
        template_name='core/login.html'
    ), name='logout'),
]