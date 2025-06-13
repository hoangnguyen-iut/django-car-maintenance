from django import template
import locale
from decimal import Decimal

register = template.Library()

@register.filter(name='vnd_format')
def vnd_format(value):
    """Định dạng số theo tiền Việt Nam VND."""
    if value is None:
        return "0 VND"
    
    # Chuyển đổi thành decimal nếu chưa phải
    if not isinstance(value, Decimal):
        value = Decimal(str(value))
    
    # Định dạng số với dấu phân cách hàng nghìn
    formatted = '{:,.0f}'.format(value).replace(',', '.')
    
    # Thêm đơn vị tiền tệ
    return f"{formatted} VND"