# Generated by Django 2.1 on 2018-10-12 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20181012_2050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='elementintown',
            name='store',
        ),
        migrations.AddField(
            model_name='elementintown',
            name='store',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='shop.StoreTown'),
        ),
    ]
