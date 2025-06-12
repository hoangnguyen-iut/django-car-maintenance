from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

class Vehicle(models.Model):
    """Model quản lý thông tin xe."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    bien_so = models.CharField(max_length=20, unique=True)
    hang_xe = models.CharField(max_length=50)
    dong_xe = models.CharField(max_length=50)
    nam_san_xuat = models.IntegerField()

    def __str__(self):
        """Trả về chuỗi đại diện cho xe."""
        return f"{self.hang_xe} {self.dong_xe} - {self.bien_so}"

class MaintenanceRecord(models.Model):
    """Model quản lý lịch sử bảo dưỡng xe."""
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_records')
    ngay_bao_duong = models.DateField()  
    ngay_den_han = models.DateField(
        verbose_name="Ngày đến hạn bảo dưỡng",
        null=True,  
        blank=True
    )
    noi_dung = models.TextField()      
    chi_phi = models.DecimalField(max_digits=12, decimal_places=0)  
    maintenance_period = models.IntegerField(default=90)  
    is_point_approved = models.BooleanField(
        default=False,
        verbose_name="Duyệt điểm tích lũy"
    )
    POINT_STATUS_CHOICES = [
        ('pending', 'Chờ duyệt'),
        ('approved', 'Đã duyệt'),
        ('rejected', 'Bị từ chối'),
    ]
    point_status = models.CharField(
        max_length=20,
        choices=POINT_STATUS_CHOICES,
        default='pending',
        verbose_name='Trạng thái tích điểm'
    )
    garage = models.ForeignKey(
        'Garage',
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Garage thực hiện"
    )

    def __str__(self):
        """Trả về chuỗi đại diện cho lịch sử bảo dưỡng."""
        return f"{self.vehicle.bien_so} - {self.ngay_bao_duong}"

    def save(self, *args, **kwargs):
        """Lưu lịch sử bảo dưỡng và tự động tính ngày đến hạn nếu chưa được set."""
        if not self.ngay_den_han and self.ngay_bao_duong:
            self.ngay_den_han = self.ngay_bao_duong + timedelta(days=365)  # mặc định 12 tháng
        super().save(*args, **kwargs)

    @property
    def days_remaining(self):
        """Tính số ngày còn lại đến hạn bảo dưỡng."""
        if not self.ngay_den_han:
            return None
        return (self.ngay_den_han - date.today()).days
        
    @property
    def days_overdue(self):
        """Tính số ngày đã quá hạn."""
        if not self.ngay_den_han:
            return None
        days = self.days_remaining
        return abs(days) if days < 0 else 0

    class Meta:
        verbose_name = "Lịch sử bảo dưỡng"
        verbose_name_plural = "Lịch sử bảo dưỡng"

class Garage(models.Model):
    """Model quản lý thông tin Garage."""
    ten_garage = models.CharField(max_length=100)
    dia_chi = models.CharField(max_length=200, default="Đang cập nhật")
    so_dien_thoai = models.CharField(max_length=20, default="Đang cập nhật")
    dich_vu = models.TextField(help_text="Danh sách dịch vụ cung cấp", default="Đang cập nhật")
    mo_ta = models.TextField(blank=True, null=True)

    def __str__(self):
        """Trả về chuỗi đại diện cho Garage."""
        return self.ten_garage

    class Meta:
        verbose_name = "Garage"
        verbose_name_plural = "Danh sách Garage"

class Appointment(models.Model):
    """Model quản lý lịch hẹn bảo dưỡng xe."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='appointments')
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE, related_name='appointments')
    ngay_gio = models.DateTimeField()
    APPOINTMENT_STATUS = [
        ('Chờ xác nhận', 'Chờ xác nhận'),  
        ('Đã xác nhận', 'Đã xác nhận'),     
        ('Từ chối', 'Từ chối'),            
        ('Hoàn thành', 'Hoàn thành'),       
        ('Đã hủy', 'Đã hủy'),               
    ]
    trang_thai = models.CharField(max_length=20, choices=APPOINTMENT_STATUS, default='Chờ xác nhận')
    ghi_chu = models.TextField(blank=True, null=True)
    ly_do = models.TextField(blank=True, null=True)

    def __str__(self):
        """Trả về chuỗi đại diện cho lịch hẹn."""
        return f"Lịch hẹn: {self.vehicle.bien_so} tại {self.garage.ten_garage} vào {self.ngay_gio}"

class ServiceCategory(models.Model):
    """Model quản lý danh mục dịch vụ của Garage."""
    ten = models.CharField(max_length=100)
    mo_ta = models.TextField(blank=True, null=True)

    def __str__(self):
        """Trả về chuỗi đại diện cho danh mục dịch vụ."""
        return self.ten

    class Meta:
        verbose_name = "Danh mục dịch vụ"
        verbose_name_plural = "Danh mục dịch vụ"

class GarageService(models.Model):
    """Model quản lý dịch vụ của Garage."""
    garage = models.ForeignKey('Garage', on_delete=models.CASCADE, related_name='chi_tiet_dich_vu')
    danh_muc = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    ten_dich_vu = models.CharField(max_length=200)
    mo_ta = models.TextField()
    gia = models.DecimalField(max_digits=12, decimal_places=0)
    thoi_gian_uoc_tinh = models.CharField(max_length=50, help_text="VD: 2-3 giờ")
    trang_thai = models.BooleanField(default=True)

    def __str__(self):

        return f"{self.garage.ten_garage} - {self.ten_dich_vu}"

    class Meta:
        verbose_name = "Dịch vụ của Garage"
        verbose_name_plural = "Dịch vụ của Garage"

class UserProfile(models.Model):
    """Model quản lý thông tin người dùng."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    USER_TYPES = [
        ('customer', 'Khách hàng'),
        ('garage_staff', 'Nhân viên Garage'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    garage = models.ForeignKey(Garage, on_delete=models.SET_NULL, null=True, blank=True)
    loyalty_points = models.IntegerField(default=0, verbose_name="Điểm tích lũy")

class PointHistory(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    maintenance_record = models.ForeignKey('MaintenanceRecord', on_delete=models.SET_NULL, null=True)
    points = models.IntegerField()  # Số điểm (dương là cộng, âm là trừ)
    action = models.CharField(max_length=20, choices=[
        ('add', 'Cộng điểm'),
        ('deduct', 'Trừ điểm'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255)
    
    class Meta:
        ordering = ['-created_at']
