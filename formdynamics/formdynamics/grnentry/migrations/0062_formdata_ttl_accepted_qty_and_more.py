# Generated by Django 4.2.3 on 2024-06-24 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grnentry', '0061_alter_processdetails_acc_qty_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='formdata',
            name='ttl_accepted_qty',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='processdetails',
            name='acc_qty',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='processdetails',
            name='rej_qty',
            field=models.IntegerField(default=0),
        ),
    ]
