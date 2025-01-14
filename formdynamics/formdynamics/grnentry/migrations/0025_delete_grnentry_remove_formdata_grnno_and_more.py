# Generated by Django 4.2.3 on 2024-04-27 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grnentry', '0024_alter_grnentry1_grnentry_ordertype_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Grnentry',
        ),
        migrations.RemoveField(
            model_name='formdata',
            name='GRNNO',
        ),
        migrations.AddField(
            model_name='formdata',
            name='grn_entry',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='grnentry.grnentry1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='processdetails',
            name='grn_entry',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='grnentry.grnentry1'),
            preserve_default=False,
        ),
    ]
