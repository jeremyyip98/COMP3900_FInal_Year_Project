# Generated by Django 3.1.7 on 2021-04-01 10:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_customer_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=400)),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='trusted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='product',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.customer'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sold_unit',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.CharField(max_length=400)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, help_text='The date and time that this response was created at.')),
                ('statement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.statement')),
            ],
        ),
        migrations.CreateModel(
            name='ProductViewCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=0)),
                ('last_viewing', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.customer')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
    ]