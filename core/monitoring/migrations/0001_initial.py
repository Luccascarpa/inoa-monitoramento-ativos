# Generated by Django 5.1.5 on 2025-01-27 04:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Asset Name')),
                ('symbol', models.CharField(max_length=10, unique=True, verbose_name='Asset Symbol')),
                ('inferior_limit', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Lower Limit')),
                ('superior_limit', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Upper Limit')),
                ('frequency', models.PositiveIntegerField(default=5, verbose_name='Checking frequency (minutes)')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PriceHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Price timestamp')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoring.asset')),
            ],
        ),
    ]
