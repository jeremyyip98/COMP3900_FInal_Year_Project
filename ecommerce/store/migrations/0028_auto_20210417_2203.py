# Generated by Django 3.1.7 on 2021-04-17 12:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0027_merge_20210416_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='imageUri',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='end_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]