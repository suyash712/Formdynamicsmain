# Generated by Django 4.2.3 on 2024-06-23 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grnentry', '0046_outsourse_receive_date_outsourse_rejected_qty_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outsourse',
            name='receive_date',
        ),
    ]
