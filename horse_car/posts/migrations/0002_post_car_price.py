# Generated by Django 5.0.6 on 2024-06-07 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='car_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
    ]
