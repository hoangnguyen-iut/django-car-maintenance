from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Garage, UserProfile

class Command(BaseCommand):
    help = 'Liên kết các tài khoản garage với Garage tương ứng'

    def handle(self, *args, **options):
        # Định nghĩa mapping giữa username và tên garage
        garage_mappings = [
            ('gara3', 'Garage Hưng Phát'),
            ('gara4', 'Garage Kim Long'),
            ('gara5', 'Garage Đại Lộc'),
            ('gara6', 'Garage Trung Tín'),
            ('gara7', 'Garage Đông Nam'),
        ]

        for username, garage_name in garage_mappings:
            try:
                # Lấy user
                user = User.objects.get(username=username)
                
                # Lấy garage
                garage = Garage.objects.get(ten_garage=garage_name)
                
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
                        f'Đã liên kết thành công tài khoản {username} với {garage_name}'
                    )
                )
                
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Không tìm thấy tài khoản {username}')
                )
            except Garage.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Không tìm thấy {garage_name}')
                )