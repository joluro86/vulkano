# Generated by Django 5.1.4 on 2025-04-09 19:14

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0003_alter_producto_codigo_interno_alter_producto_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='fecha_ingreso',
        ),
        migrations.AddField(
            model_name='producto',
            name='creado_por',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producto',
            name='modificado_por',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
