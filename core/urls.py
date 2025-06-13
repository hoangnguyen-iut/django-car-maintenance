from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

urlpatterns = [
    # Chuyển hướng về trang chào mừng thay vì trang đăng nhập
    path('', lambda request: redirect('welcome'), name='home'),
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
    path('login/', views.custom_login, name='login'),
    path('accounts/login/', views.custom_login, name='accounts_login'),
    path('register/', views.register, name='register'),  # Thay đổi từ accounts/register/
    path('logout/', auth_views.LogoutView.as_view(
        next_page='/login/',
        template_name='core/login.html'
    ), name='logout'),
    path('garage/appointments/', views.manage_appointments, name='manage_appointments'),
    path('garage/appointments/<int:pk>/update/', views.update_appointment_status, name='update_appointment_status'),
    path('garage/dashboard/', views.garage_dashboard, name='garage_dashboard'),
    path('garage/appointment/<int:appointment_id>/', views.handle_appointment, name='handle_appointment'),
    path('welcome/', views.welcome, name='welcome'),
    # Comment out or remove duplicate login/register URLs
    # path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    # path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('accounts/register/', views.register, name='register'),
]

urlpatterns += [
    path('garage/point-approvals/', 
         views.point_approvals_list, 
         name='point_approvals_list'),
    path('garage/point-approvals/approve/<int:record_id>/',
         views.approve_point_by_staff,
         name='approve_point'),
    path('garage/point-approvals/reject/<int:record_id>/',
         views.reject_point_by_staff,
         name='reject_point'),
    # Thêm dòng này nếu muốn giữ tên trong template
    path('garage/point-approvals/reject_staff/<int:record_id>/',
         views.reject_point_by_staff,
         name='reject_point_by_staff'),
    path('points/history/', views.point_history, name='point_history'),
]