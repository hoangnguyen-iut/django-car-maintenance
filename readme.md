Dưới đây là hướng dẫn từng bước tạo môi trường Django trong VSCode và code dự án “Hệ thống Theo dõi Bảo Dưỡng Xe” sử dụng SQLite. Hướng dẫn này sẽ giúp bạn thiết lập môi trường, tạo project, app, định nghĩa các model và chạy server để kiểm tra kết quả qua giao diện quản trị.

---

## 1. Chuẩn bị ban đầu

- **Cài đặt Python:**  
  Đảm bảo rằng Python (phiên bản 3.7 trở lên) đã được cài trên máy tính của bạn. Nếu chưa, hãy tải Python từ [python.org](https://www.python.org/).

- **Cài đặt Visual Studio Code:**  
  Tải VSCode từ [trang chủ VSCode](https://code.visualstudio.com/). Cài đặt extension Python (Microsoft) để hỗ trợ code và debugging.

---

## 2. Tạo thư mục dự án và môi trường ảo

1. **Tạo thư mục dự án:**  
   Mở VSCode, mở Terminal tích hợp (nhấn `Ctrl + ~`) hoặc sử dụng menu View > Terminal.  
   Tạo thư mục cho dự án (ví dụ: `django-car-maintenance`):

   ```bash
   mkdir django-car-maintenance
   cd django-car-maintenance
   ```

2. **Tạo môi trường ảo:**  
   Dùng lệnh sau để tạo một virtual environment (gọi tên là `env`):

   ```bash
   python -m venv env
   ```

3. **Kích hoạt môi trường ảo:**  
   - Trên Windows:

     ```bash
     env\Scripts\activate
     ```

   - Trên macOS/Linux:

     ```bash
     source env/bin/activate
     ```

   Sau khi kích hoạt, bạn sẽ thấy tên môi trường (ví dụ, `(env)`) xuất hiện ở đầu dòng lệnh.

4. **Cài đặt Django:**  
   Cài đặt Django thông qua pip:

   ```bash
   pip install django
   ```

---

## 3. Tạo Project Django

1. **Tạo project mới:**  
   Sử dụng lệnh `django-admin startproject` để tạo project. Chúng ta sử dụng tên project là `car_maintenance`.

   ```bash
   django-admin startproject car_maintenance .
   ```

   **Lưu ý:** Dấu chấm ở cuối lệnh giúp tạo các tệp cấu hình ngay trong thư mục hiện hành thay vì tạo một thư mục con.

2. **Cấu trúc thư mục dự án:**  
   Sau khi tạo, bạn sẽ thấy các file như:
   
   - `manage.py`
   - Thư mục con `car_maintenance/` chứa các file cấu hình (settings, urls, wsgi, …).

---

## 4. Tạo App “core” cho dự án

1. **Tạo app mới:**  
   Dùng lệnh sau để tạo app, ở đây đặt tên là `core`:

   ```bash
   python manage.py startapp core
   ```

2. **Thêm app vào cấu hình:**  
   Mở file `car_maintenance/settings.py` và thêm `'core'` vào danh sách `INSTALLED_APPS`:

   ```python
   INSTALLED_APPS = [
       # Các apps mặc định của Django
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',

       # Ứng dụng của bạn
       'core',
   ]
   ```

---

## 5. Tạo các Model trong App “core”

Dự án "Hệ thống Theo dõi Bảo Dưỡng Xe" bao gồm 5 bảng:  
- **Users (Người dùng):** Dùng sẵn model User của Django.  
- **Vehicles (Xe của người dùng)**  
- **MaintenanceRecords (Lịch sử bảo dưỡng xe)**  
- **Garages (Trung tâm bảo dưỡng xe)**  
- **Appointments (Lịch hẹn bảo dưỡng)**  

Mở file `core/models.py` và định nghĩa các model như sau:

```python
from django.db import models
from django.contrib.auth.models import User

class Vehicle(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    bien_so = models.CharField(max_length=20, unique=True)
    hang_xe = models.CharField(max_length=50)
    dong_xe = models.CharField(max_length=50)
    nam_san_xuat = models.IntegerField()

    def __str__(self):
        return f"{self.hang_xe} {self.dong_xe} - {self.bien_so}"

class MaintenanceRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_records')
    ngay_bao_duong = models.DateField()
    noi_dung = models.TextField(help_text="Miêu tả công việc bảo dưỡng (thay dầu, kiểm tra phanh, v.v.)")
    chi_phi = models.DecimalField(max_digits=10, decimal_places=2)
    ghi_chu = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Bảo dưỡng xe {self.vehicle.bien_so} ngày {self.ngay_bao_duong}"

class Garage(models.Model):
    ten_garage = models.CharField(max_length=100)
    dia_chi = models.CharField(max_length=200)
    so_dien_thoai = models.CharField(max_length=20)
    dich_vu = models.TextField(help_text="Danh sách dịch vụ cung cấp")
    mo_ta = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.ten_garage

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='appointments')
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE, related_name='appointments')
    ngay_gio = models.DateTimeField()
    trang_thai = models.CharField(max_length=50, default='Chờ xác nhận')
    ghi_chu = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Lịch hẹn: {self.vehicle.bien_so} tại {self.garage.ten_garage} vào {self.ngay_gio}"
```

Lưu lại file, các model này sẽ tạo tương ứng 4 bảng (ngoại trừ user) trong cơ sở dữ liệu SQLite.

---

## 6. Áp dụng Migration cho Database

1. **Tạo migration cho các model:**  
   Trong Terminal, chạy:

   ```bash
   python manage.py makemigrations
   ```

2. **Chạy migration:**  
   Áp dụng các thay đổi vào database:

   ```bash
   python manage.py migrate
   ```

---

## 7. Đăng ký Model vào Admin

Để quản lý dữ liệu thông qua giao diện Django Admin, bạn cần đăng ký các model trong file `core/admin.py`.

Mở file `core/admin.py` và thêm:

```python
from django.contrib import admin
from .models import Vehicle, MaintenanceRecord, Garage, Appointment

admin.site.register(Vehicle)
admin.site.register(MaintenanceRecord)
admin.site.register(Garage)
admin.site.register(Appointment)
```

Lưu lại file.

---

## 8. Tạo Superuser và Chạy Server

1. **Tạo superuser để truy cập admin:**  
   Chạy lệnh sau và nhập thông tin (username, email, password):

   ```bash
   python manage.py createsuperuser
   ```

2. **Chạy server:**  
   Khởi động server phát triển của Django:

   ```bash
   python manage.py runserver
   ```

3. **Kiểm tra:**  
   Mở trình duyệt và truy cập `http://127.0.0.1:8000/admin` để đăng nhập vào giao diện quản trị với tài khoản superuser bạn vừa tạo.

---

## 9. Các Bước Tiếp Theo (Views, Templates, Forms)

Sau khi hoàn thiện backend và thiết lập các model, bạn có thể:

- **Xây dựng Views và URLs:** Tạo các view để hiển thị danh sách xe, lịch sử bảo dưỡng, garage… và định nghĩa các URL tương ứng trong file `core/urls.py` (đừng quên include nó trong `car_maintenance/urls.py`).

- **Tạo Template:** Sử dụng Django Template Language để tạo giao diện thân thiện cho người dùng.

- **Xử lý Forms:** Xây dựng Django Forms để người dùng có thể nhập dữ liệu như đặt lịch hẹn bảo dưỡng hoặc ghi nhận bảo dưỡng.

- **Tích hợp các chức năng nâng cao:** Ví dụ, gửi email nhắc lịch bảo dưỡng, tích hợp Google Maps API để hiển thị vị trí garage, v.v.

---

## 10. Một số Mẹo Khi Sử Dụng VSCode

- **Debugging:** VSCode có hỗ trợ debugging cho Python. Bạn có thể tạo file cấu hình `.vscode/launch.json` để chạy và debug server Django dễ dàng.
- **Terminal tích hợp:** Sử dụng terminal tích hợp trong VSCode để thực hiện lệnh Django như `python manage.py migrate`, `python manage.py runserver` mà không cần chuyển qua cửa sổ khác.
- **Tiện ích mở rộng:** Cài đặt các extension hỗ trợ Python, Django (ví dụ: “Django Template” hay “Python Docstring Generator”) để tăng hiệu suất code.

---

Với các bước trên, bạn đã có một môi trường phát triển Django hoàn chỉnh trong VSCode cho dự án “Hệ thống Theo dõi Bảo Dưỡng Xe”. Hãy thử thực hiện từng bước và kiểm tra kết quả qua Django Admin. Nếu bạn muốn tìm hiểu thêm về xây dựng các view, template hay tích hợp API (ví dụ Django REST Framework), bạn có thể mở rộng dự án theo nhu cầu.

Bạn có cảm thấy phần nào cần được giải thích rõ hơn hoặc muốn mở rộng chức năng nào không?

Dưới đây là hướng dẫn chi tiết từng bước để xây dựng các view, thiết lập URL, xây dựng các template hiển thị thông tin (danh sách xe, lịch sử bảo dưỡng, garage) và một ví dụ về form (thêm xe mới) cho dự án “Hệ thống Theo dõi Bảo Dưỡng Xe” sử dụng Django. Bạn hãy làm theo các bước dưới đây:

---

## 1. Tạo Views trong File `core/views.py`

Trước tiên, bạn mở file `core/views.py` và định nghĩa các view cơ bản. Ví dụ, bạn có thể tạo 3 view để hiển thị danh sách xe, lịch sử bảo dưỡng và danh sách garage. Ngoài ra, mình sẽ thêm thêm view để xử lý form thêm xe mới.

```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Vehicle, MaintenanceRecord, Garage
from .forms import VehicleForm

# Hiển thị danh sách xe
@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.filter(owner=request.user)
    return render(request, 'core/vehicle_list.html', {'vehicles': vehicles})

# Hiển thị lịch sử bảo dưỡng xe (có thể lọc theo owner nếu cần)
@login_required
def maintenance_list(request):
    # Lấy tất cả lịch sử bảo dưỡng cho các xe của user đăng nhập
    records = MaintenanceRecord.objects.filter(vehicle__owner=request.user)
    return render(request, 'core/maintenance_list.html', {'records': records})

# Hiển thị danh sách các Garage
def garage_list(request):
    garages = Garage.objects.all()
    return render(request, 'core/garage_list.html', {'garages': garages})

# Ví dụ view xử lý Form thêm xe mới
@login_required
def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user   # gán chủ xe là user hiện tại
            vehicle.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    return render(request, 'core/add_vehicle.html', {'form': form})
```

Ở đây, mình sử dụng decorator `@login_required` cho các view cần thiết bảo mật (để chỉ người dùng đã đăng nhập mới sử dụng được). Bạn có thể tùy chỉnh thêm theo nhu cầu.

---

## 2. Định Nghĩa URL trong File `core/urls.py`

Tạo file `core/urls.py` (nếu chưa có) và định nghĩa các URL cho các view vừa tạo:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/add/', views.add_vehicle, name='add_vehicle'),
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('garages/', views.garage_list, name='garage_list'),
]
```

Sau đó, bạn cần include các URL này vào file `car_maintenance/urls.py` trong thư mục project. Mở file `car_maintenance/urls.py` và sửa lại như sau:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Include các URL của app core
]
```

---

## 3. Tạo Các Template

Trong cấu trúc Django, các template thường được đặt trong thư mục `templates` bên trong app. Tạo thư mục theo đường dẫn:  
`core/templates/core/`  
Trong thư mục này, tạo các file template tương ứng:

### a. Template hiển thị danh sách xe: `vehicle_list.html`

```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Danh Sách Xe</title>
</head>
<body>
    <h1>Danh Sách Xe Của Bạn</h1>
    <a href="{% url 'add_vehicle' %}">Thêm xe mới</a>
    <ul>
        {% for vehicle in vehicles %}
            <li>
                {{ vehicle.hang_xe }} {{ vehicle.dong_xe }} - {{ vehicle.bien_so }}
            </li>
        {% empty %}
            <li>Không có xe nào được đăng ký.</li>
        {% endfor %}
    </ul>
</body>
</html>
```

### b. Template hiển thị lịch sử bảo dưỡng: `maintenance_list.html`

```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Lịch Sử Bảo Dưỡng Xe</title>
</head>
<body>
    <h1>Lịch Sử Bảo Dưỡng Xe</h1>
    <ul>
        {% for record in records %}
            <li>
                Xe: {{ record.vehicle.bien_so }} |
                Ngày: {{ record.ngay_bao_duong }} |
                Nội dung: {{ record.noi_dung }} |
                Chi phí: {{ record.chi_phi }}
            </li>
        {% empty %}
            <li>Chưa có bản ghi bảo dưỡng nào.</li>
        {% endfor %}
    </ul>
</body>
</html>
```

### c. Template hiển thị danh sách garage: `garage_list.html`

```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Danh Sách Garage</title>
</head>
<body>
    <h1>Danh Sách Các Garage</h1>
    <ul>
        {% for garage in garages %}
            <li>
                {{ garage.ten_garage }} - Địa chỉ: {{ garage.dia_chi }} - SĐT: {{ garage.so_dien_thoai }}
            </li>
        {% empty %}
            <li>Chưa có garage nào.</li>
        {% endfor %}
    </ul>
</body>
</html>
```

### d. Template cho Form thêm xe mới: `add_vehicle.html`

```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Thêm Xe Mới</title>
</head>
<body>
    <h1>Thêm Xe Mới</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Thêm Xe</button>
    </form>
    <a href="{% url 'vehicle_list' %}">Quay về danh sách xe</a>
</body>
</html>
```

Bạn có thể tạo thêm các template cho các chức năng khác tùy theo nhu cầu mở rộng dự án.

---

## 4. Tạo Form cho Vehicle

Để người dùng có thể thêm xe mới, hãy tạo file `core/forms.py`:

```python
from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        # Nếu muốn người dùng tự nhập biển số, hãng xe, dòng xe và năm sản xuất:
        fields = ['bien_so', 'hang_xe', 'dong_xe', 'nam_san_xuat']
```

Form này sẽ được sử dụng trong view `add_vehicle` để render giao diện nhập liệu, xử lý kiểm tra dữ liệu và lưu dữ liệu vào cơ sở dữ liệu.

---

## 5. Kiểm Tra và Chạy Dự Án

1. **Chạy Migration (nếu chưa chạy):**  
   Trong terminal, chạy:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Tạo User (nếu chưa có) và Login:**  
   Tạo tài khoản superuser (hoặc user bình thường) để thử nghiệm:
   ```bash
   python manage.py createsuperuser
   ```

3. **Chạy Server:**  
   ```bash
   python manage.py runserver
   ```
   Truy cập các URL:
   - Danh sách xe: `http://127.0.0.1:8000/vehicles/`
   - Thêm xe mới: `http://127.0.0.1:8000/vehicles/add/`
   - Lịch sử bảo dưỡng: `http://127.0.0.1:8000/maintenance/`
   - Danh sách garage: `http://127.0.0.1:8000/garages/`

Nếu bạn đăng nhập, bạn sẽ có thể xem giao diện và kiểm tra chức năng thêm xe, hiển thị dữ liệu,…

---

## 6. Các Bước Mở Rộng Sau Này

- **Tạo thêm View để chỉnh sửa, xoá thông tin:** Xây dựng các view cho việc update và delete cho từng model.  
- **Phân trang (Pagination):** Nếu số lượng dữ liệu tăng dần, có thể áp dụng phân trang cho các danh sách.  
- **Tích hợp AJAX:** Để cải thiện trải nghiệm người dùng khi thực hiện các thao tác không cần tải lại trang.  
- **Tích hợp Django REST Framework:** Cho việc cung cấp API, hướng tới việc phát triển ứng dụng di động trong tương lai.

---

Bây giờ, bạn đã có một cấu trúc cơ bản cho các view, URL và template cùng với form xử lý dữ liệu. Bạn có thể tùy chỉnh giao diện và mở rộng chức năng theo mục tiêu cụ thể của đồ án. Bạn cảm thấy phần nào cần được giải thích thêm hoặc bổ sung tính năng nào khác không?