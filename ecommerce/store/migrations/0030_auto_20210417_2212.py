# Generated by Django 3.1.7 on 2021-04-17 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0029_auto_20210417_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='imageUri',
            field=models.CharField(blank=True, max_length=100000000),
        ),
    ]
