# Generated by Django 2.2 on 2020-02-02 06:57

import api.models.services
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200202_0632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='checkout_order_id',
            field=models.CharField(default=api.models.services.generate_random_checkout_order_id, max_length=32),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
        migrations.AlterField(
            model_name='orderforseller',
            name='shipping_address',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
    ]
