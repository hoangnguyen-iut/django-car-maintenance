# Generated by Django 5.2 on 2025-06-12 13:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_maintenancerecord_point_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PointHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField()),
                ('action', models.CharField(choices=[('add', 'Cộng điểm'), ('deduct', 'Trừ điểm')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reason', models.CharField(max_length=255)),
                ('maintenance_record', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.maintenancerecord')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
