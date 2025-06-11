from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import MaintenanceRecord
from .tinh_diem import tru_diem_tich_luy

@receiver(pre_delete, sender=MaintenanceRecord)
def handle_maintenance_delete(sender, instance, **kwargs):
    """Xử lý trừ điểm khi xóa bản ghi bảo dưỡng."""
    if instance.is_point_approved:
        tru_diem_tich_luy(instance)