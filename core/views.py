from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Vehicle, MaintenanceRecord, Garage, GarageService, ServiceCategory, Appointment
from .forms import VehicleForm, MaintenanceRecordForm, AppointmentForm
from django.contrib.auth.forms import UserCreationForm
from datetime import date

# Hiển thị danh sách xe
@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.filter(owner=request.user)
    return render(request, 'core/vehicle_list.html', {'vehicles': vehicles})

# Hiển thị lịch sử bảo dưỡng xe (có thể lọc theo owner nếu cần)
@login_required
def maintenance_list(request):
    records = MaintenanceRecord.objects.filter(
        vehicle__owner=request.user
    ).order_by('-ngay_bao_duong')  # Sort by maintenance date instead
    
    return render(request, 'core/maintenance_list.html', {
        'records': records,
        'today': date.today()
    })

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

@login_required
def add_maintenance(request):
    if request.method == 'POST':
        form = MaintenanceRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.save()
            messages.success(request, 'Đã thêm lịch sử bảo dưỡng thành công!')
            return redirect('maintenance_list')
    else:
        form = MaintenanceRecordForm()
        # Chỉ hiển thị xe của user hiện tại
        form.fields['vehicle'].queryset = Vehicle.objects.filter(owner=request.user)
    return render(request, 'core/add_maintenance.html', {'form': form})

@login_required
def edit_maintenance(request, pk):
    record = get_object_or_404(MaintenanceRecord, pk=pk, vehicle__owner=request.user)
    
    if request.method == 'POST':
        form = MaintenanceRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thành công!')
            return redirect('maintenance_list')
    else:
        form = MaintenanceRecordForm(instance=record)
        
    return render(request, 'core/edit_maintenance.html', {
        'form': form,
        'record': record
    })

@login_required
def delete_maintenance(request, pk):
    record = get_object_or_404(MaintenanceRecord, pk=pk, vehicle__owner=request.user)
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Đã xóa lịch sử bảo dưỡng thành công!')
        return redirect('maintenance_list')
    return render(request, 'core/delete_maintenance.html', {'record': record})

@login_required
def create_appointment(request, garage_id):
    garage = get_object_or_404(Garage, pk=garage_id)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.garage = garage
            appointment.trang_thai = 'Chờ xác nhận'
            appointment.save()
            messages.success(request, 'Đặt lịch hẹn thành công!')
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
        # Chỉ hiển thị xe của user hiện tại
        form.fields['vehicle'].queryset = Vehicle.objects.filter(owner=request.user)
    
    return render(request, 'core/create_appointment.html', {
        'form': form,
        'garage': garage
    })

@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(
        user=request.user
    ).order_by('-ngay_gio')
    return render(request, 'core/appointment_list.html', {
        'appointments': appointments
    })
