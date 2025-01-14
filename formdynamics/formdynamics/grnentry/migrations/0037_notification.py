# Generated by Django 4.2.3 on 2024-06-13 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grnentry', '0036_outsourse_completed_time_alter_outsourse_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('calibration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grnentry.calibration')),
            ],
        ),
    ]
