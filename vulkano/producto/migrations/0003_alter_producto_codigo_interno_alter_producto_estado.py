# Generated by Django 5.1.4 on 2025-04-09 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0002_alter_producto_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='codigo_interno',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='producto',
            name='estado',
            field=models.CharField(choices=[('disponible', 'Disponible'), ('alquilado', 'Alquilado')], default='disponible', max_length=20),
        ),
    ]
