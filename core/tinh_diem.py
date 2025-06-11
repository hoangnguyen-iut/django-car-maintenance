from math import floor
from django.db import transaction
from .models import UserProfile

def cong_diem_tich_luy(maintenance_record):
    """
    Tính và cộng điểm tích lũy cho chủ xe.
    
    Args:
        maintenance_record: Bản ghi bảo dưỡng cần tính điểm
    Returns:
        int: Số điểm được cộng hoặc 0 nếu không thỏa điều kiện
    """
    # Kiểm tra điều kiện duyệt điểm
    if not maintenance_record.is_point_approved:
        return 0
        
    # Tính điểm (100.000 VND = 10 điểm)
    points = floor(float(maintenance_record.chi_phi) / 10000)
    
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
        
    return points

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