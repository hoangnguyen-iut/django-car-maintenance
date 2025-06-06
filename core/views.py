from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Vehicle, MaintenanceRecord, Garage, GarageService, ServiceCategory
from .forms import VehicleForm
from django.contrib.auth.forms import UserCreationForm

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
            vehicle.owner = request.user
            vehicle.save()
            messages.success(request, f'Xe {vehicle.bien_so} đã được thêm thành công!')
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    return render(request, 'core/add_vehicle.html', {'form': form})

@login_required
def edit_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, f'Xe {vehicle.bien_so} đã được cập nhật!')
            return redirect('vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'core/edit_vehicle.html', {'form': form, 'vehicle': vehicle})

@login_required
def delete_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, owner=request.user)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, f'Xe {vehicle.bien_so} đã được xóa!')
        return redirect('vehicle_list')
    return render(request, 'core/delete_vehicle.html', {'vehicle': vehicle})

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

def garage_detail(request, pk):
    garage = get_object_or_404(Garage, pk=pk)
    services = GarageService.objects.filter(garage=garage, trang_thai=True)
    categories = ServiceCategory.objects.filter(garageservice__garage=garage).distinct()
    
    context = {
        'garage': garage,
        'categories': categories,
        'services': services
    }
    return render(request, 'core/garage_detail.html', context)
