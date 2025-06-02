from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        # Nếu muốn người dùng tự nhập biển số, hãng xe, dòng xe và năm sản xuất:
        fields = ['bien_so', 'hang_xe', 'dong_xe', 'nam_san_xuat']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Tên đăng nhập'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Mật khẩu'
    }))
