# Generated by Django 4.2.3 on 2024-06-25 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grnentry', '0062_formdata_ttl_accepted_qty_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outsourse1',
            name='accepted_qty',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='outsourse1',
            name='rejected_qty',
            field=models.IntegerField(default=0),
        ),
    ]
