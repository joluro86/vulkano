# Generated by Django 5.1.4 on 2025-07-14 19:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alquiler', '0022_delete_reservainventario'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AbonoAlquiler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('metodo_pago', models.CharField(blank=True, max_length=50)),
                ('observaciones', models.TextField(blank=True)),
                ('alquiler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='abonos', to='alquiler.alquiler')),
                ('registrado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LiquidacionAlquiler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('total_liquidado', models.DecimalField(decimal_places=2, max_digits=10)),
                ('observaciones', models.TextField(blank=True)),
                ('alquiler', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='liquidacion', to='alquiler.alquiler')),
                ('liquidado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
