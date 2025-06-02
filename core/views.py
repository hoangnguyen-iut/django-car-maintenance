from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Vehicle, MaintenanceRecord, Garage
from .forms import VehicleForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Hiển thị danh sách xe
@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.filter(owner=request.user)
    return render(request, 'core/vehicle_list.html', {'vehicles': vehicles})

# Hiển thị lịch sử bảo dưỡng xe (có thể lọc theo owner nếu cần)
@login_required
def maintenance_list(request):
    # Lấy tất cả lịch sử bảo dưỡng cho các xe của user đăng nhập
    records = MaintenanceRecord.objects.filter(vehicle__owner=request.user)
    return render(request, 'core/maintenance_list.html', {'records': records})

# Hiển thị danh sách các Garage
def garage_list(request):
    garages = Garage.objects.all()
    return render(request, 'core/garage_list.html', {'garages': garages})

# Ví dụ view xử lý Form thêm xe mới
@login_required
def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user   # gán chủ xe là user hiện tại
            vehicle.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    return render(request, 'core/add_vehicle.html', {'form': form})

def home(request):
    # Chuyển hướng về trang đăng nhập admin của Django
    return redirect('/admin/login/')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
