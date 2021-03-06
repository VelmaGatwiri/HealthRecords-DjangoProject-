# Generated by Django 3.2.9 on 2022-01-25 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedicalApp', '0004_hospitalprofile_abouthospital'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='Hospital_Description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospital',
            name='Hospital_Image',
            field=models.ImageField(default='default.png', upload_to='hospital_pics'),
        ),
        migrations.DeleteModel(
            name='HospitalProfile',
        ),
    ]
