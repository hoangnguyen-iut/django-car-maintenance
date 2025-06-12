from math import floor
from django.db import transaction
from .models import UserProfile, PointHistory

def record_point_history(user, maintenance_record, points, action, reason):
    """Ghi lại lịch sử điểm"""
    PointHistory.objects.create(
        user=user,
        maintenance_record=maintenance_record,
        points=points,
        action=action,
        reason=reason
    )

def cong_diem_tich_luy(maintenance_record):
    """
    Tính và cộng điểm tích lũy cho chủ xe.
    """
    try:
        # Debug print
        print(f"Processing points for record {maintenance_record.id}")
        print(f"Chi phí: {maintenance_record.chi_phi}")
        
        # Tính điểm (100.000 VND = 10 điểm)
        points = floor(float(maintenance_record.chi_phi) / 10000)
        print(f"Calculated points: {points}")
        
        # Sử dụng transaction để đảm bảo tính toàn vẹn dữ liệu
        with transaction.atomic():
            # Lấy hoặc tạo profile cho chủ xe
            profile, created = UserProfile.objects.get_or_create(
                user=maintenance_record.vehicle.owner,
                defaults={'loyalty_points': 0}
            )
            
            # Cộng điểm
            profile.loyalty_points += points
            profile.save()
            
            # Ghi lịch sử cộng điểm
            record_point_history(
                user=maintenance_record.vehicle.owner,
                maintenance_record=maintenance_record,
                points=points,
                action='add',
                reason=f'Bảo dưỡng xe {maintenance_record.vehicle.bien_so}'
            )
            
            print(f"Updated points for user {profile.user.username}: {profile.loyalty_points}")
            
        return points
        
    except Exception as e:
        print(f"Error in cong_diem_tich_luy: {str(e)}")
        raise

def tru_diem_tich_luy(maintenance_record):
    """
    Trừ điểm tích lũy khi xóa bản ghi bảo dưỡng.
    
    Args:
        maintenance_record: Bản ghi bảo dưỡng bị xóa
    """
    if not maintenance_record.is_point_approved:
        return
        
    # Tính điểm cần trừ (100.000 VND = 10 điểm)
    points_to_deduct = floor(float(maintenance_record.chi_phi) / 10000)
    
    with transaction.atomic():
        profile = maintenance_record.vehicle.owner.userprofile
        profile.loyalty_points = max(0, profile.loyalty_points - points_to_deduct)
        profile.save()
        
        # Ghi lịch sử trừ điểm
        record_point_history(
            user=maintenance_record.vehicle.owner,
            maintenance_record=maintenance_record,
            points=-points_to_deduct,
            action='deduct',
            reason=f'Hủy bảo dưỡng xe {maintenance_record.vehicle.bien_so}'
        )