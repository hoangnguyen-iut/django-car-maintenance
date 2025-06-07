from django import forms
from .models import Vehicle, MaintenanceRecord, Appointment

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['bien_so', 'hang_xe', 'dong_xe', 'nam_san_xuat']
        labels = {
            'bien_so': 'Biển số xe',
            'hang_xe': 'Hãng xe', 
            'dong_xe': 'Dòng xe',
            'nam_san_xuat': 'Năm sản xuất'
        }
        widgets = {
            'bien_so': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ''
            }),
            'hang_xe': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ''
            }),
            'dong_xe': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': ''
            }),
            'nam_san_xuat': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': ''
            }),
        }

class MaintenanceRecordForm(forms.ModelForm):
    MAINTENANCE_PERIODS = [
        (90, '3 tháng'),
        (180, '6 tháng'),
        (270, '9 tháng'),
        (365, '1 năm'),
    ]
    
    maintenance_period = forms.IntegerField(
        initial=90,
        widget=forms.Select(choices=MAINTENANCE_PERIODS, attrs={'class': 'form-select'})
    )

    class Meta:
        model = MaintenanceRecord
        fields = ['vehicle', 'ngay_bao_duong', 'noi_dung', 'chi_phi', 'maintenance_period']
        labels = {
            'vehicle': 'Chọn xe',
            'ngay_bao_duong': 'Ngày bảo dưỡng',
            'noi_dung': 'Nội dung bảo dưỡng',
            'chi_phi': 'Chi phí (VNĐ)'
        }
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'ngay_bao_duong': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'noi_dung': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'chi_phi': forms.NumberInput(attrs={'class': 'form-control'})
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['vehicle', 'ngay_gio', 'ghi_chu']
        labels = {
            'vehicle': 'Chọn xe',
            'ngay_gio': 'Ngày giờ hẹn',
            'ghi_chu': 'Ghi chú thêm'
        }
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'ngay_gio': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                }
            ),
            'ghi_chu': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            })
        }
