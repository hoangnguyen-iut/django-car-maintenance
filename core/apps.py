from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Cấu hình ứng dụng core cho hệ thống quản lý bảo dưỡng xe."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """Import signals khi app khởi động."""
        import core.signals
