# Generated by Django 2.1 on 2018-10-20 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20181012_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elementintown',
            name='elem',
            field=models.ManyToManyField(related_name='element_details', to='shop.Elements'),
        ),
    ]
