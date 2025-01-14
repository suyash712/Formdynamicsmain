# Generated by Django 4.2.3 on 2024-06-23 11:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('grnentry', '0045_supplier'),
    ]

    operations = [
        migrations.AddField(
            model_name='outsourse',
            name='receive_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='outsourse',
            name='rejected_qty',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='outsourse',
            name='supplier_process_name',
            field=models.CharField(default=121, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='outsourse',
            name='out_date',
            field=models.DateField(),
        ),
    ]
