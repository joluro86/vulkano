# Generated by Django 5.1.4 on 2025-04-09 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0005_remove_producto_activo_alter_producto_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='stock',
        ),
    ]
