# Generated by Django 4.2.3 on 2024-06-23 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grnentry', '0052_outsourse1_receive_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='outsourse1',
            name='dc',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
