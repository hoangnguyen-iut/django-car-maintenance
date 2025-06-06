from django import forms
from .models import Vehicle

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
