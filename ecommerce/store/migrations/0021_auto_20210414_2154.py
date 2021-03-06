# Generated by Django 3.1.7 on 2021-04-14 11:54

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_auto_20210414_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidder',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bidder', to='store.product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='end_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 4, 14, 11, 54, 51, 891346, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='highest_bidder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='highest_bidder', to='store.customer'),
        ),
    ]
