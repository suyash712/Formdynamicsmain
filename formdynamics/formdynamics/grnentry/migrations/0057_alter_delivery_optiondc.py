# Generated by Django 4.2.3 on 2024-06-24 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grnentry', '0056_alter_delivery_optiondc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='OPTIONDC',
            field=models.CharField(max_length=200),
        ),
    ]
