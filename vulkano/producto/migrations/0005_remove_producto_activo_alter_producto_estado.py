# Generated by Django 5.1.4 on 2025-04-09 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0004_remove_producto_fecha_ingreso_producto_creado_por_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='activo',
        ),
        migrations.AlterField(
            model_name='producto',
            name='estado',
            field=models.CharField(choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='disponible', max_length=20),
        ),
    ]
