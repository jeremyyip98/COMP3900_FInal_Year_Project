# Generated by Django 3.1.7 on 2021-04-14 13:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_auto_20210414_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='end_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 4, 14, 13, 30, 51, 943127, tzinfo=utc), null=True),
        ),
    ]
