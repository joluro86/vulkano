# Generated by Django 5.1.4 on 2025-07-07 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0007_movimientoinventario_cliente_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimientoinventario',
            name='estado',
            field=models.CharField(choices=[('borrador', 'Borrador'), ('confirmado', 'Confirmado'), ('anulado', 'Anulado')], default='borrador', max_length=20),
        ),
    ]
