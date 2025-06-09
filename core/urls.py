"""URL Configuration cho ứng dụng core."""

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

urlpatterns = [
    # URLs cho trang chủ và quản lý xe
    path('', lambda request: redirect('welcome'), name='home'),
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/add/', views.add_vehicle, name='add_vehicle'),
    
    # URLs cho quản lý bảo dưỡng
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/add/', views.add_maintenance, name='add_maintenance'),
    path('maintenance/<int:pk>/edit/', views.edit_maintenance, name='edit_maintenance'),
    path('maintenance/<int:pk>/delete/', views.delete_maintenance, name='delete_maintenance'),
    
    # URLs cho quản lý garage
    path('garages/', views.garage_list, name='garage_list'),
    path('garage/<int:pk>/', views.garage_detail, name='garage_detail'),
    path('garage/dashboard/', views.garage_dashboard, name='garage_dashboard'),
    
    # URLs cho quản lý xe
    path('vehicles/<int:pk>/edit/', views.edit_vehicle, name='edit_vehicle'),
    path('vehicles/<int:pk>/delete/', views.delete_vehicle, name='delete_vehicle'),
    
    # URLs cho quản lý lịch hẹn
    path('garage/<int:garage_id>/appointment/', views.create_appointment, name='create_appointment'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('garage/appointments/', views.manage_appointments, name='manage_appointments'),
    path('garage/appointments/<int:pk>/update/', views.update_appointment_status, name='update_appointment_status'),
    path('garage/appointment/<int:appointment_id>/', views.handle_appointment, name='handle_appointment'),
    
    # URLs cho xác thực người dùng
    path('login/', auth_views.LoginView.as_view(
        template_name='core/login.html',
        next_page='/vehicles/'
    ), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='/login/',
        template_name='core/login.html'
    ), name='logout'),
    
    # URL trang chào mừng
    path('welcome/', views.welcome, name='welcome'),
    
    # Comment out or remove duplicate login/register URLs
    # path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    # path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('accounts/register/', views.register, name='register'),
]