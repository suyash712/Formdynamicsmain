# Generated by Django 5.0.6 on 2024-06-21 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grnentry', '0040_grnentry1_customername_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formdata',
            name='exptime',
        ),
        migrations.RemoveField(
            model_name='formdata',
            name='image',
        ),
        migrations.RemoveField(
            model_name='formdata',
            name='quantitycheck',
        ),
        migrations.RemoveField(
            model_name='formdata',
            name='report',
        ),
        migrations.AlterField(
            model_name='grnentry1',
            name='grnentry_EXPTIME',
            field=models.DateField(max_length=200),
        ),
        migrations.AlterField(
            model_name='processdetails',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='processdetails',
            name='start_date',
            field=models.DateField(),
        ),
    ]