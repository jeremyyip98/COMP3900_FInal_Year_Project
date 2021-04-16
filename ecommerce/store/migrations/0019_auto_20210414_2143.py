# Generated by Django 3.1.7 on 2021-04-14 11:43

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_auto_20210405_2058'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('edited', models.BooleanField(default=False)),
                ('rating', models.PositiveIntegerField()),
                ('text', models.TextField(max_length=1000)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.customer')),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='end_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 4, 14, 11, 43, 23, 296349, tzinfo=utc), null=True),
        ),
        migrations.CreateModel(
            name='ReviewReact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked', models.BooleanField(default=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.customer')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reacts', to='store.productreview')),
            ],
        ),
        migrations.AddField(
            model_name='productreview',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='store.product'),
        ),
        migrations.AddConstraint(
            model_name='productreview',
            constraint=models.UniqueConstraint(fields=('product', 'author'), name='User can only leave one review per product'),
        ),
    ]