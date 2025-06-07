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

![8817a0e7-38c5-413f-a28e-92d62391b6ab](file:///C:/Users/Admin/Pictures/Typedown/8817a0e7-38c5-413f-a28e-92d62391b6ab.png)

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

![4af79048-9277-4645-8320-1247ac0c1f92](file:///C:/Users/Admin/Pictures/Typedown/4af79048-9277-4645-8320-1247ac0c1f92.png)

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

![dd77ddb9-c070-4773-8534-c2085449f4a0](file:///C:/Users/Admin/Pictures/Typedown/dd77ddb9-c070-4773-8534-c2085449f4a0.png)

---

```sql
-- Chèn dữ liệu vào bảng vehicle
INSERT INTO core_vehicle (owner_id, bien_so, hang_xe, dong_xe, nam_san_xuat)
VALUES
    (1, '29A-12345', 'Toyota', 'Camry', 2019),
    (1, '30F-67890', 'Honda', 'Civic', 2021),
    (2, '51G-54321', 'Ford', 'Ranger', 2020);

-- Chèn dữ liệu vào bảng garage
INSERT INTO core_garage (ten_garage, dia_chi, so_dien_thoai, dich_vu, mo_ta)
VALUES
    ('Gara Minh Anh', '123 Đường Láng, Hà Nội', '0987654321', 'Thay dầu, sửa phanh, kiểm tra động cơ', 'Gara uy tín với hơn 10 năm kinh nghiệm'),
    ('Gara Thành Công', '456 Nguyễn Trãi, TP.HCM', '0912345678', 'Bảo dưỡng định kỳ, sơn xe, thay lốp', 'Dịch vụ chất lượng cao');

-- Chèn dữ liệu vào bảng maintenancerecord
INSERT INTO core_maintenancerecord (vehicle_id, ngay_bao_duong, noi_dung, chi_phi, ghi_chu)
VALUES
    (1, '2025-01-15', 'Thay dầu động cơ, kiểm tra phanh', 1500000.00, 'Dầu tổng hợp cao cấp'),
    (1, '2025-03-20', 'Thay lốp trước, cân chỉnh bánh', 3200000.00, NULL),
    (2, '2025-02-10', 'Kiểm tra hệ thống điện, thay ắc quy', 2500000.00, 'Ắc quy chính hãng'),
    (3, '2025-04-05', 'Bảo dưỡng định kỳ 10,000km', 1800000.00, 'Kiểm tra toàn bộ hệ thống');

-- Chèn dữ liệu vào bảng appointment
INSERT INTO core_appointment (user_id, vehicle_id, garage_id, ngay_gio, trang_thai, ghi_chu)
VALUES
    (1, 1, 1, '2025-06-10 09:00:00', 'Chờ xác nhận', 'Kiểm tra động cơ định kỳ'),
    (1, 2, 2, '2025-06-15 14:30:00', 'Đã xác nhận', 'Yêu cầu thay dầu và kiểm tra lốp'),
    (2, 3, 1, '2025-06-20 11:00:00', 'Chờ xác nhận', NULL);
```

![55dc5aea-09f2-43c0-89d1-04a28135deaa](file:///C:/Users/Admin/Pictures/Typedown/55dc5aea-09f2-43c0-89d1-04a28135deaa.png)

![e1272d98-3f15-471c-a1f2-9ccdea82de47](file:///C:/Users/Admin/Pictures/Typedown/e1272d98-3f15-471c-a1f2-9ccdea82de47.png)

![56388d3d-2db9-42d3-ae7f-898748612862](file:///C:/Users/Admin/Pictures/Typedown/56388d3d-2db9-42d3-ae7f-898748612862.png)

![27b7e9fe-fe34-4373-adff-3acfb1ace7ee](file:///C:/Users/Admin/Pictures/Typedown/27b7e9fe-fe34-4373-adff-3acfb1ace7ee.png)

![87e8835a-8135-4cce-a1f1-a0cd797cb921](file:///C:/Users/Admin/Pictures/Typedown/87e8835a-8135-4cce-a1f1-a0cd797cb921.png)

## 6. Áp dụng Migration cho Database



1. **Tạo migration cho các model:**  

   Trong Terminal, chạy:



   ```bash

   python manage.py makemigrations

   ```

![01f5027d-84c2-47ac-b4de-1ef44e19d81d](file:///C:/Users/Admin/Pictures/Typedown/01f5027d-84c2-47ac-b4de-1ef44e19d81d.png)

2. **Chạy migration:**  

   Áp dụng các thay đổi vào database:



   ```bash

   python manage.py migrate

   ```

![657ecf3d-501c-4c69-a631-2d99f5e7b71f](file:///C:/Users/Admin/Pictures/Typedown/657ecf3d-501c-4c69-a631-2d99f5e7b71f.png)

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

![bb1757c7-690d-48fa-901b-d4297285c4d2](file:///C:/Users/Admin/Pictures/Typedown/bb1757c7-690d-48fa-901b-d4297285c4d2.png)

Lưu lại file.



---



## 8. Tạo Superuser và Chạy Server



1. **Tạo superuser để truy cập admin:**  

   Chạy lệnh sau và nhập thông tin (username, email, password):



   ```bash

   python manage.py createsuperuser

   ```

![5c56adbf-b4da-4ba6-a4e8-894a63855140](file:///C:/Users/Admin/Pictures/Typedown/5c56adbf-b4da-4ba6-a4e8-894a63855140.png)

pass: Admin@123

2. **Chạy server:**  

   Khởi động server phát triển của Django:



   ```bash

   python manage.py runserver

   ```

    ![dbbed3bb-7325-4ad5-91df-7d159b9f5cf8](file:///C:/Users/Admin/Pictures/Typedown/dbbed3bb-7325-4ad5-91df-7d159b9f5cf8.png)*không được tắt tab này*

3. **Kiểm tra:**  

   Mở trình duyệt và truy cập `http://127.0.0.1:8000/admin` để đăng nhập vào giao diện quản trị với tài khoản superuser bạn vừa tạo.

username: admin
pass: Admin@123

![7c794f69-79b1-4e78-bb63-3bd40994e6af](file:///C:/Users/Admin/Pictures/Typedown/7c794f69-79b1-4e78-bb63-3bd40994e6af.png)

![86815879-6e07-4a2a-81be-2bb7a33e8c2c](file:///C:/Users/Admin/Pictures/Typedown/86815879-6e07-4a2a-81be-2bb7a33e8c2c.png)

---



## 9. Các Bước Tiếp Theo (Views, Templates, Forms)



Sau khi hoàn thiện backend và thiết lập các model, bạn có thể:



- **Xây dựng Views và URLs:** Tạo các view để hiển thị danh sách xe, lịch sử bảo dưỡng, garage… và định nghĩa các URL tương ứng trong file `core/urls.py` (đừng quên include nó trong `car_maintenance/urls.py`).
  
  

- **Tạo Template:** Sử dụng Django Template Language để tạo giao diện thân thiện cho người dùng.
  
  

- **Xử lý Forms:** Xây dựng Django Forms để người dùng có thể nhập dữ liệu như đặt lịch hẹn bảo dưỡng hoặc ghi nhận bảo dưỡng.
  
  

- **Tích hợp các chức năng nâng cao:** Ví dụ, gửi email nhắc lịch bảo dưỡng, tích hợp Google Maps API để hiển thị vị trí garage, v.v.
  
  

---



Dưới đây là hướng dẫn chi tiết từng bước để xây dựng các view, thiết lập URL, xây dựng các template hiển thị thông tin (danh sách xe, lịch sử bảo dưỡng, garage) và một ví dụ về form (thêm xe mới) cho dự án “Hệ thống Theo dõi Bảo Dưỡng Xe” sử dụng Django. Bạn hãy làm theo các bước dưới đây:



---



## 10. Tạo Views trong File `core/views.py`



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



## 12. Định Nghĩa URL trong File `core/urls.py`



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



## 13. Tạo Các Template



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



## 14. Tạo Form cho Vehicle



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



## 15. Kiểm Tra và Chạy Dự Án



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



## 16. Các Bước Mở Rộng Sau Này



- **Tạo thêm View để chỉnh sửa, xoá thông tin:** Xây dựng các view cho việc update và delete cho từng model.  

- **Phân trang (Pagination):** Nếu số lượng dữ liệu tăng dần, có thể áp dụng phân trang cho các danh sách.  

- **Tích hợp AJAX:** Để cải thiện trải nghiệm người dùng khi thực hiện các thao tác không cần tải lại trang.  

- **Tích hợp Django REST Framework:** Cho việc cung cấp API, hướng tới việc phát triển ứng dụng di động trong tương lai.
  
  

---



Bây giờ, bạn đã có một cấu trúc cơ bản cho các view, URL và template cùng với form xử lý dữ liệu. Bạn có thể tùy chỉnh giao diện và mở rộng chức năng theo mục tiêu cụ thể của đồ án. Bạn cảm thấy phần nào cần được giải thích thêm hoặc bổ sung tính năng nào khác không?





# Hướng dẫn người dùng sử dụng ứng dụng: "Hệ thống Theo dõi Bảo Dưỡng Xe,"

Trình bày từng bước rõ ràng như sau: 

## **1. Đăng ký và đăng nhập**

* Truy cập trang đăng nhập tại `http://localhost:8000/accounts/login/`.

* Nếu chưa có tài khoản, chọn **Đăng ký** để tạo tài khoản mới.

* Sau khi đăng ký, đăng nhập bằng email và mật khẩu.

**2. Quản lý xe cá nhân**
-------------------------

* Truy cập `http://localhost:8000/vehicles/` để xem danh sách xe của bạn.

* Nhấn **“Thêm xe mới”** để nhập biển số, hãng xe, dòng xe, năm sản xuất.

* Xe đã đăng ký sẽ xuất hiện trong danh sách để bạn dễ theo dõi.

**3. Kiểm tra lịch sử bảo dưỡng**
---------------------------------

* Vào `http://localhost:8000/maintenance/` để xem danh sách các lần bảo dưỡng.

* Hệ thống hiển thị xe nào đã bảo dưỡng, ngày bảo trì, chi phí và nội dung bảo dưỡng.

* Bạn có thể kiểm tra lịch sử để lên kế hoạch bảo dưỡng định kỳ.

**4. Tìm garage và đặt lịch hẹn**
---------------------------------

* Truy cập `http://localhost:8000/garages/` để xem danh sách garage bảo dưỡng xe gần bạn.

* Nhấn vào một garage để xem chi tiết dịch vụ.

* Đặt lịch hẹn bảo dưỡng xe bằng cách chọn xe và thời gian bảo dưỡng.

**5. Nhận thông báo nhắc lịch bảo dưỡng**
-----------------------------------------

* Hệ thống sẽ tự động nhắc lịch bảo dưỡng khi đến hạn.

* Bạn có thể kiểm tra lịch bảo dưỡng tiếp theo trên trang **Lịch sử bảo dưỡng**.

**6. Đăng xuất khi hoàn tất**
-----------------------------

* Nếu bạn muốn đăng xuất, vào `http://localhost:8000/accounts/logout/`.

* Khi đăng nhập lại, dữ liệu của bạn vẫn được lưu.

### **Lưu ý:**

* Ứng dụng yêu cầu đăng nhập trước khi sử dụng một số tính năng.

* Dữ liệu được lưu trữ an toàn, chỉ tài khoản của bạn có thể xem thông tin xe và lịch bảo dưỡng.
