from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Vehicle, MaintenanceRecord, Garage, GarageService, ServiceCategory, Appointment, UserProfile, PointHistory
from .forms import VehicleForm, MaintenanceRecordForm, AppointmentForm
from django.contrib.auth.forms import UserCreationForm
from datetime import date, timedelta, datetime
from math import floor
from django.views.decorators.http import require_POST
from .tinh_diem_tich_luy import cong_diem_tich_luy
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


@login_required
def vehicle_list(request):
    """Hiển thị danh sách xe của người dùng"""
    vehicles = Vehicle.objects.filter(owner=request.user)
    return render(request, 'core/vehicle_list.html', {'vehicles': vehicles})


@login_required 
def maintenance_list(request):
    """Hiển thị danh sách bảo dưỡng và điểm tích lũy."""
    records = MaintenanceRecord.objects.filter(
        vehicle__owner=request.user
    ).order_by('-ngay_bao_duong')
    
    # Lấy hoặc tạo profile cho user
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={'loyalty_points': 0}
    )
    
    return render(request, 'core/maintenance_list.html', {
        'records': records,
        'total_points': profile.loyalty_points
    })

"""Hiển thị danh sách Garage"""        
def garage_list(request):
    garages = Garage.objects.all()
    return render(request, 'core/garage_list.html', {'garages': garages})


@login_required
def add_vehicle(request):
    """Thêm xe mới cho người dùng"""
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
    """Chỉnh sửa thông tin xe của người dùng"""
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
    """Xóa xe của người dùng"""
    vehicle = get_object_or_404(Vehicle, pk=pk, owner=request.user)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, f'Xe {vehicle.bien_so} đã được xóa!')
        return redirect('vehicle_list')
    return render(request, 'core/delete_vehicle.html', {'vehicle': vehicle})

def home(request):
    """Chuyển hướng về trang đăng nhập admin của Django"""
    return redirect('/admin/login/')

def register(request):
    """Đăng ký tài khoản người dùng mới"""
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
    """Hiển thị chi tiết Garage và các dịch vụ"""
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
    """Thêm lịch sử bảo dưỡng cho xe"""
    """Kiểm tra xem người dùng đã có xe nào chưa"""
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
    """Chỉnh sửa lịch sử bảo dưỡng"""
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
        
        # Lọc danh sách xe chỉ hiển thị xe của user hiện tại
        user_vehicles = Vehicle.objects.filter(owner=request.user)
        form.fields['vehicle'].queryset = user_vehicles
        
    return render(request, 'core/edit_maintenance.html', {'form': form})

@login_required
def delete_maintenance(request, pk):
    """Xóa bản ghi bảo dưỡng."""
    record = get_object_or_404(MaintenanceRecord, pk=pk, vehicle__owner=request.user)
    
    if request.method == 'POST':
        points_to_deduct = floor(float(record.chi_phi) / 10000) if record.is_point_approved else 0
        record.delete()
        
        if points_to_deduct > 0:
            messages.warning(
                request, 
                f'Đã xóa bản ghi bảo dưỡng. {points_to_deduct} điểm tích lũy đã bị trừ.'
            )
        else:
            messages.success(request, 'Đã xóa bản ghi bảo dưỡng.')
        
        return redirect('maintenance_list')
    
    return render(request, 'core/delete_maintenance.html', {'record': record})

@login_required
def create_appointment(request, garage_id):
    """Tạo lịch hẹn với Garage"""
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
    """Hiển thị danh sách lịch hẹn của người dùng"""
    appointments = Appointment.objects.filter(
        user=request.user
    ).order_by('-ngay_gio')
    return render(request, 'core/appointment_list.html', {
        'appointments': appointments
    })

def is_garage_staff(user):
    """Kiểm tra xem người dùng có phải là nhân viên Garage hay không"""
    return hasattr(user, 'userprofile') and user.userprofile.user_type == 'garage_staff'

@user_passes_test(is_garage_staff)
def manage_appointments(request):
    """Quản lý lịch hẹn của Garage"""
    garage = request.user.userprofile.garage
    appointments = Appointment.objects.filter(garage=garage).order_by('-ngay_gio')
    return render(request, 'core/manage_appointments.html', {'appointments': appointments})

@user_passes_test(is_garage_staff)
def update_appointment_status(request, pk):
    """Cập nhật trạng thái lịch hẹn"""    
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
    """Hiển thị bảng điều khiển của Garage với các lịch hẹn chờ xác nhận"""
    """Chỉ hiển thị các lịch hẹn có trạng thái 'Chờ xác nhận'"""
    garage = request.user.userprofile.garage
    pending_appointments = Appointment.objects.filter(
        garage=garage,
        trang_thai='Chờ xác nhận' 
    ).select_related('user', 'vehicle').order_by('ngay_gio')
    
    # Debug print
    print(f"Searching appointments for garage: {garage}")
    print(f"Found appointments: {pending_appointments.count()}")
    print(f"All appointments statuses: {list(Appointment.objects.filter(garage=garage).values_list('trang_thai', flat=True))}")
    
    return render(request, 'core/garage_dashboard.html', {
        'appointments': pending_appointments,
        'garage': garage
    })

@require_POST
@user_passes_test(lambda u: hasattr(u, 'userprofile') and u.userprofile.user_type == 'garage_staff')
def handle_appointment(request, appointment_id):
    """Xử lý lịch hẹn từ bảng điều khiển của Garage"""
    """Xác nhận hoặc từ chối lịch hẹn"""
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

@user_passes_test(lambda u: hasattr(u, 'userprofile') and u.userprofile.user_type == 'garage_staff')
def point_approvals_list(request):
    """Hiển thị danh sách chờ duyệt điểm."""
    garage = request.user.userprofile.garage
    pending_records = MaintenanceRecord.objects.filter(
        garage=garage,
        is_point_approved=False,
        is_point_rejected=False  # Thêm điều kiện này để loại bỏ các bản ghi đã từ chối
    ).select_related(
        'vehicle',
        'vehicle__owner'
    ).order_by('-ngay_bao_duong')
    
    return render(request, 'core/garage/point_approvals.html', {
        'records': pending_records
    })

@user_passes_test(lambda u: hasattr(u, 'userprofile') and u.userprofile.user_type == 'garage_staff')
def approve_point_by_staff(request, record_id):
    """Duyệt điểm cho bản ghi bảo dưỡng."""
    garage = request.user.userprofile.garage
    record = get_object_or_404(MaintenanceRecord, id=record_id, garage=garage)
    
    if record.is_point_approved:
        messages.error(request, 'Bản ghi này đã được duyệt điểm!')
        return redirect('point_approvals_list')

    try:
        points = cong_diem_tich_luy(record)
        record.is_point_approved = True
        record.save()

        messages.success(
            request, 
            f'Đã duyệt và cộng {points} điểm tích lũy cho bản ghi #{record.id}'
        )
    except Exception as e:
        messages.error(request, f'Lỗi khi duyệt điểm: {str(e)}')
        
    return redirect('point_approvals_list')

@user_passes_test(lambda u: hasattr(u, 'userprofile') and u.userprofile.user_type == 'garage_staff')
def reject_point_by_staff(request, record_id):
    """Từ chối tích điểm cho bản ghi bảo dưỡng."""
    garage = request.user.userprofile.garage
    record = get_object_or_404(MaintenanceRecord, id=record_id, garage=garage)
    
    if record.is_point_approved:
        messages.error(request, 'Không thể từ chối bản ghi đã được duyệt!')
        return redirect('point_approvals_list')
    
    # Cập nhật trạng thái
    record.is_point_rejected = True
    record.is_point_approved = False
    record.point_status = 'rejected'  # Cập nhật trạng thái hiển thị
    record.save()
    
    messages.success(request, f'Đã từ chối cộng điểm cho bản ghi #{record.id}')
    return redirect('point_approvals_list')

@login_required
def point_history(request):
    """Xem lịch sử điểm tích lũy"""
    history = PointHistory.objects.filter(user=request.user)
    
    # Lấy hoặc tạo profile cho user
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={'loyalty_points': 0}
    )
    # Lấy lịch sử điểm tích lũy
    return render(request, 'core/point_history.html', {
        'history': history,
        'total_points': profile.loyalty_points  # Thêm điểm tích lũy vào context
    })

def welcome(request):
    """Trang chào mừng"""
    return render(request, 'core/welcome.html')

def custom_login(request):
    """Đăng nhập người dùng"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Kiểm tra xem người dùng có tồn tại không
        user_exists = User.objects.filter(username=username).exists()
        
        if not user_exists:
            messages.error(request, 'Tài khoản chưa được đăng ký')
            return render(request, 'core/login.html')
        
        # Thực hiện xác thực người dùng
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('vehicle_list')  # Hoặc nơi bạn muốn chuyển hướng sau khi đăng nhập
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không chính xác')
            return render(request, 'core/login.html')
    
    return render(request, 'core/login.html')
