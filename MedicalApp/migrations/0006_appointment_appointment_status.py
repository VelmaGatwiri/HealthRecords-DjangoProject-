# Generated by Django 3.2.9 on 2022-01-25 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedicalApp', '0005_auto_20220125_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='Appointment_Status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Cancelled', 'Cancelled'), ('Successful', 'Successful'), ('Postponed', 'Postponed')], default='Pending', max_length=20, null=True),
        ),
    ]
