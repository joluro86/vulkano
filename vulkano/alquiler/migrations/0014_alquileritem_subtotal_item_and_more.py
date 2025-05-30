# Generated by Django 5.1.4 on 2025-05-22 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alquiler', '0013_alter_alquiler_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='alquileritem',
            name='subtotal_item',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='alquileritem',
            name='precio_dia',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
