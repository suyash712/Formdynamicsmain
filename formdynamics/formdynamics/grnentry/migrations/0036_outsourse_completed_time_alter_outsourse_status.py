# Generated by Django 4.2.3 on 2024-06-13 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grnentry', '0035_outsourse'),
    ]

    operations = [
        migrations.AddField(
            model_name='outsourse',
            name='completed_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='outsourse',
            name='status',
            field=models.CharField(default='pending', max_length=200),
        ),
    ]
