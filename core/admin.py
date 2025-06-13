from django.contrib import admin
from .models import Vehicle, MaintenanceRecord, Garage, Appointment, ServiceCategory, GarageService, UserProfile
from django.contrib import messages

admin.site.register(Vehicle)


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    """Quản lý bản ghi bảo trì trong trang admin."""
    list_display = ['vehicle', 'ngay_bao_duong', 'chi_phi', 'is_point_approved']
    list_filter = ['is_point_approved']
    
    def save_model(self, request, obj, form, change):
        """Xử lý tích điểm khi admin duyệt."""
        try:
            # Kiểm tra nếu trạng thái duyệt điểm thay đổi
            if change and 'is_point_approved' in form.changed_data and obj.is_point_approved:
                from .tinh_diem import cong_diem_tich_luy
                points = cong_diem_tich_luy(obj)
                if points > 0:
                    messages.success(
                        request, 
                        f'Đã cộng {points} điểm tích lũy cho {obj.vehicle.owner.username}'
                    )
            super().save_model(request, obj, form, change)
        except Exception as e:
            messages.error(request, f'Lỗi khi xử lý tích điểm: {str(e)}')

admin.site.register(Garage)

admin.site.register(Appointment)

admin.site.register(UserProfile)

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    """Quản lý danh mục dịch vụ trong trang admin."""
    list_display = ['ten', 'mo_ta']
    search_fields = ['ten']

@admin.register(GarageService)
class GarageServiceAdmin(admin.ModelAdmin):
    """Quản lý chi tiết dịch vụ của garage trong trang admin."""
    list_display = ['garage', 'danh_muc', 'ten_dich_vu', 'gia', 'trang_thai']
    list_filter = ['garage', 'danh_muc', 'trang_thai']
    search_fields = ['ten_dich_vu', 'mo_ta']