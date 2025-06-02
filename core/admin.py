from django.contrib import admin

from .models import Vehicle, MaintenanceRecord, Garage, Appointment

admin.site.register(Vehicle)

admin.site.register(MaintenanceRecord)

admin.site.register(Garage)

admin.site.register(Appointment)