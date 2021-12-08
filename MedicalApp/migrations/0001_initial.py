# Generated by Django 3.2.9 on 2021-12-07 10:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Hospital_Name', models.CharField(max_length=100)),
                ('Registration_Date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
