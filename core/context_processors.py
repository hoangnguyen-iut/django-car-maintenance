from datetime import datetime
from .models import MaintenanceRecord

def notification_processor(request):
    """Xử lý và trả về thông báo về các lịch bảo dưỡng đã quá hạn."""
    if not request.user.is_authenticated:
        return {'notifications': []}
    
    today = datetime.now().date()
    overdue_records = MaintenanceRecord.objects.filter(
        vehicle__owner=request.user,
        ngay_den_han__lt=today
    ).select_related('vehicle')
    
    notifications = []
    for record in overdue_records:
        days_overdue = (today - record.ngay_den_han).days
        notifications.append({
            'vehicle': record.vehicle.bien_so,
            'content': record.noi_dung,
            'days_overdue': days_overdue
        })
    
    return {'notifications': notifications}
