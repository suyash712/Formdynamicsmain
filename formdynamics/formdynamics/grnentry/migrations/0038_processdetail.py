# Generated by Django 4.2.3 on 2024-06-17 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grnentry', '0037_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('quantity', models.IntegerField()),
                ('completed', models.BooleanField(default=False)),
                ('form_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grnentry.formdata')),
            ],
        ),
    ]