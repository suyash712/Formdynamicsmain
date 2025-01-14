# Generated by Django 4.2.3 on 2024-06-08 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grnentry', '0031_calibration'),
    ]

    operations = [
        migrations.CreateModel(
            name='master_component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('drawing_no', models.CharField(max_length=200)),
                ('revision_no', models.CharField(max_length=200)),
                ('drawing_pdf', models.FileField(upload_to='master_drawing/')),
            ],
        ),
    ]
