# Generated by Django 5.1.3 on 2025-02-12 09:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0011_alter_customuser_user_type_alter_doctor_model_fees'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor_model',
            name='user',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[(1, 'admin'), (3, 'patient'), (2, 'doc')], default=None, max_length=20),
        ),
        migrations.AlterField(
            model_name='doctor_model',
            name='username',
            field=models.OneToOneField(default='doctor_model', max_length=100, on_delete=django.db.models.deletion.CASCADE, to='hospital.customuser'),
        ),
    ]
