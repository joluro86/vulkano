# Generated by Django 5.1.4 on 2025-05-19 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alquiler', '0004_alquiler_cliente'),
    ]

    operations = [
        migrations.AddField(
            model_name='alquiler',
            name='descuento_porcentaje',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Descuento general aplicado al total del alquiler', max_digits=5),
        ),
    ]
