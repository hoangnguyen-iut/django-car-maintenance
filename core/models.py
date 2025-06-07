from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

class Vehicle(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    bien_so = models.CharField(max_length=20, unique=True)
    hang_xe = models.CharField(max_length=50)
    dong_xe = models.CharField(max_length=50)
    nam_san_xuat = models.IntegerField()

    def __str__(self):
        return f"{self.hang_xe} {self.dong_xe} - {self.bien_so}"

class MaintenanceRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_records')
    ngay_bao_duong = models.DateField()  # Vietnamese field name for service_date
    ngay_den_han = models.DateField(
        verbose_name="Ngày đến hạn bảo dưỡng",
        null=True,  # cho phép null cho dữ liệu cũ
        blank=True
    )
    noi_dung = models.TextField()        # Vietnamese field name for description
    chi_phi = models.DecimalField(max_digits=12, decimal_places=0)  # Vietnamese field name for cost

    def __str__(self):
        return f"{self.vehicle.bien_so} - {self.ngay_bao_duong}"

    def save(self, *args, **kwargs):
        # Tự động tính ngày đến hạn nếu chưa được set
        if not self.ngay_den_han and self.ngay_bao_duong:
            self.ngay_den_han = self.ngay_bao_duong + timedelta(days=365)  # mặc định 12 tháng
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Lịch sử bảo dưỡng"
        verbose_name_plural = "Lịch sử bảo dưỡng"

class Garage(models.Model):
    ten_garage = models.CharField(max_length=100)
    dia_chi = models.CharField(max_length=200, default="Đang cập nhật")
    so_dien_thoai = models.CharField(max_length=20, default="Đang cập nhật")
    dich_vu = models.TextField(help_text="Danh sách dịch vụ cung cấp", default="Đang cập nhật")
    mo_ta = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.ten_garage

    class Meta:
        verbose_name = "Garage"
        verbose_name_plural = "Danh sách Garage"

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='appointments')
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE, related_name='appointments')
    ngay_gio = models.DateTimeField()
    trang_thai = models.CharField(max_length=50, default='Chờ xác nhận')
    ghi_chu = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Lịch hẹn: {self.vehicle.bien_so} tại {self.garage.ten_garage} vào {self.ngay_gio}"

class ServiceCategory(models.Model):
    ten = models.CharField(max_length=100)
    mo_ta = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.ten

    class Meta:
        verbose_name = "Danh mục dịch vụ"
        verbose_name_plural = "Danh mục dịch vụ"

class GarageService(models.Model):
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
