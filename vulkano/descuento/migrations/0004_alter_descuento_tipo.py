# Generated by Django 5.1.4 on 2025-05-23 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('descuento', '0003_alter_descuento_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='descuento',
            name='tipo',
            field=models.CharField(choices=[('oferta', 'Oferta'), ('convenio', 'Convenio')], max_length=20),
        ),
    ]
