from django.contrib import admin

from .models import Vehicle, MaintenanceRecord, Garage, Appointment, ServiceCategory, GarageService

admin.site.register(Vehicle)

admin.site.register(MaintenanceRecord)

admin.site.register(Garage)

admin.site.register(Appointment)

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['ten', 'mo_ta']
    search_fields = ['ten']

@admin.register(GarageService)
class GarageServiceAdmin(admin.ModelAdmin):
    list_display = ['garage', 'danh_muc', 'ten_dich_vu', 'gia', 'trang_thai']
    list_filter = ['garage', 'danh_muc', 'trang_thai']
    search_fields = ['ten_dich_vu', 'mo_ta']