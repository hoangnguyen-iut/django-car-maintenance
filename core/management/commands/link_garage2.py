from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Garage, UserProfile

class Command(BaseCommand):
    help = 'Liên kết tài khoản gara2 với Gara Thành Công'

    def handle(self, *args, **options):
        try:
            # Lấy user gara2
            user = User.objects.get(username='gara2')
            
            # Lấy Gara Thành Công
            garage = Garage.objects.get(ten_garage='Gara Thành Công')
            
            # Cập nhật hoặc tạo UserProfile
            profile, created = UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'user_type': 'garage_staff',
                    'garage': garage
                }
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Đã liên kết thành công tài khoản gara2 với {garage.ten_garage}'
                )
            )
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Không tìm thấy tài khoản gara2')
            )
        except Garage.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Không tìm thấy Gara Thành Công')
            )