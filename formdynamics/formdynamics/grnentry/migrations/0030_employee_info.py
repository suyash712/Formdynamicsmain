# Generated by Django 4.2.3 on 2024-06-08 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grnentry', '0029_material'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('Designation', models.CharField(max_length=200)),
                ('aadhar_no', models.CharField(max_length=200)),
                ('mobile_no', models.CharField(max_length=200)),
            ],
        ),
    ]
