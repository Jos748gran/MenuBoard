# Generated by Django 5.1.4 on 2025-01-14 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estadisticas', '0009_remove_estadistica_mesa_mesa_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estadistica_mesa',
            name='factura_list',
        ),
        migrations.RemoveField(
            model_name='estadistica_mesero',
            name='factura_list',
        ),
        migrations.RemoveField(
            model_name='estadistica_producto',
            name='item_factura_list',
        ),
        migrations.AddField(
            model_name='estadistica_mesa',
            name='factura_list',
            field=models.ManyToManyField(blank=True, related_name='estadistica_mesa', to='Estadisticas.factura'),
        ),
        migrations.AddField(
            model_name='estadistica_mesero',
            name='factura_list',
            field=models.ManyToManyField(blank=True, related_name='estadistica_mesero', to='Estadisticas.factura'),
        ),
        migrations.AddField(
            model_name='estadistica_producto',
            name='item_factura_list',
            field=models.ManyToManyField(blank=True, related_name='estadistica_producto', to='Estadisticas.item_factura'),
        ),
    ]
