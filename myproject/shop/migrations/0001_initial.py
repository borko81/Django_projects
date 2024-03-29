# Generated by Django 2.1 on 2018-10-12 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ElementIntown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Elements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('info', models.TextField()),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('vip', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='StoreTown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storename', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='elements',
            name='group_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Groups'),
        ),
        migrations.AddField(
            model_name='elementintown',
            name='elem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Elements'),
        ),
        migrations.AddField(
            model_name='elementintown',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.StoreTown'),
        ),
    ]
