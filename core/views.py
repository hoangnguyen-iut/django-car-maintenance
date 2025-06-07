from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Vehicle, MaintenanceRecord, Garage, GarageService, ServiceCategory, Appointment
from .forms import VehicleForm, MaintenanceRecordForm, AppointmentForm
from django.contrib.auth.forms import UserCreationForm
from datetime import date, timedelta, datetime

# Hiển thị danh sách xe
@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.filter(owner=request.user)
    return render(request, 'core/vehicle_list.html', {'vehicles': vehicles})

# Hiển thị lịch sử bảo dưỡng xe (có thể lọc theo owner nếu cần)
@login_required
def maintenance_list(request):
    today = datetime.now().date()
    records = MaintenanceRecord.objects.filter(
        vehicle__owner=request.user
    ).order_by('-ngay_bao_duong')
    
    for record in records:
        if record.ngay_den_han:
            days_diff = (record.ngay_den_han - today).days
            record.days_remaining = days_diff
    
    return render(request, 'core/maintenance_list.html', {
        'records': records,
        'today': today,
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
            messages.success(request, 'Đăng ký tài khoản thành công! Vui lòng đăng nhập.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

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
    # Check if user has any vehicles
    user_vehicles = Vehicle.objects.filter(owner=request.user)
    if not user_vehicles.exists():
        messages.warning(request, 'Bạn cần thêm ít nhất một xe trước khi thêm lịch sử bảo dưỡng!')
        return redirect('add_vehicle')

    if request.method == 'POST':
        form = MaintenanceRecordForm(request.POST)
        if form.is_valid():
            maintenance = form.save(commit=False)
            maintenance.maintenance_period = form.cleaned_data['maintenance_period']
            maintenance.ngay_den_han = maintenance.ngay_bao_duong + timedelta(days=maintenance.maintenance_period)
            maintenance.save()
            messages.success(request, 'Thêm mới lịch sử bảo dưỡng thành công!')
            return redirect('maintenance_list')
    else:
        form = MaintenanceRecordForm()
        # Filter vehicles for current user
        form.fields['vehicle'].queryset = user_vehicles

    return render(request, 'core/add_maintenance.html', {'form': form})

@login_required
def edit_maintenance(request, pk):
    record = get_object_or_404(MaintenanceRecord, pk=pk, vehicle__owner=request.user)
    if request.method == 'POST':
        form = MaintenanceRecordForm(request.POST, instance=record)
        if form.is_valid():
            maintenance = form.save(commit=False)
            days = int(form.cleaned_data['maintenance_period'])
            maintenance.ngay_den_han = maintenance.ngay_bao_duong + timedelta(days=days)
            maintenance.save()
            messages.success(request, 'Cập nhật thành công!')
            return redirect('maintenance_list')
    else:
        # Tính ngược lại số ngày để chọn chu kỳ
        if record.ngay_den_han and record.ngay_bao_duong:
            days = (record.ngay_den_han - record.ngay_bao_duong).days
            initial_period = min((p[0] for p in MaintenanceRecordForm.MAINTENANCE_PERIODS if p[0] >= days), default=365)
        else:
            initial_period = 180
        form = MaintenanceRecordForm(instance=record, initial={'maintenance_period': initial_period})
    return render(request, 'core/edit_maintenance.html', {'form': form})

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
            appointment.trang_thai = 'Chờ xác nhận'  # Updated to match model's status
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

def is_garage_staff(user):
    return hasattr(user, 'userprofile') and user.userprofile.user_type == 'garage_staff'

@user_passes_test(is_garage_staff)
def manage_appointments(request):
    garage = request.user.userprofile.garage
    appointments = Appointment.objects.filter(garage=garage).order_by('-ngay_gio')
    return render(request, 'core/manage_appointments.html', {'appointments': appointments})

@user_passes_test(is_garage_staff)
def update_appointment_status(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, garage=request.user.userprofile.garage)
    if request.method == 'POST':
        status = request.POST.get('status')
        ly_do = request.POST.get('ly_do', '')
        appointment.trang_thai = status
        appointment.ly_do = ly_do
        appointment.save()
        messages.success(request, 'Cập nhật trạng thái lịch hẹn thành công!')
    return redirect('manage_appointments')

@user_passes_test(lambda u: hasattr(u, 'userprofile') and u.userprofile.user_type == 'garage_staff')
def garage_dashboard(request):
    garage = request.user.userprofile.garage
    pending_appointments = Appointment.objects.filter(
        garage=garage,
        trang_thai='Chờ xác nhận'  # Updated to match model's status
    ).select_related('user', 'vehicle').order_by('ngay_gio')
    
    # Debug print
    print(f"Searching appointments for garage: {garage}")
    print(f"Found appointments: {pending_appointments.count()}")
    print(f"All appointments statuses: {list(Appointment.objects.filter(garage=garage).values_list('trang_thai', flat=True))}")
    
    return render(request, 'core/garage_dashboard.html', {
        'appointments': pending_appointments,
        'garage': garage
    })

from django.views.decorators.http import require_POST

@require_POST
@user_passes_test(lambda u: hasattr(u, 'userprofile') and u.userprofile.user_type == 'garage_staff')
def handle_appointment(request, appointment_id):
    garage = request.user.userprofile.garage
    appointment = get_object_or_404(Appointment, id=appointment_id, garage=garage)
    action = request.POST.get('action')
    
    if action == 'confirm':
        appointment.trang_thai = 'confirmed'
        messages.success(request, 'Đã xác nhận lịch hẹn')
    elif action == 'reject':
        appointment.trang_thai = 'rejected'
        appointment.ly_do = request.POST.get('ly_do', '')
        messages.warning(request, 'Đã từ chối lịch hẹn')
    
    appointment.save()
    return redirect('garage_dashboard')

def welcome(request):
    return render(request, 'core/welcome.html')
