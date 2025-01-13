# Generated by Django 5.1.4 on 2025-01-13 03:49

import django.core.validators
import django.db.models.deletion
import pedidos.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Historial',
                'verbose_name_plural': 'Historiales',
            },
        ),
        migrations.CreateModel(
            name='Mesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacidad', models.PositiveIntegerField(default=1)),
                ('disponible', models.BooleanField(default=True, editable=False)),
                ('numero', models.PositiveIntegerField(editable=False, unique=True)),
            ],
            options={
                'verbose_name': 'Mesa',
                'verbose_name_plural': 'Mesas',
            },
        ),
        migrations.CreateModel(
            name='Plato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'verbose_name': 'Plato',
                'verbose_name_plural': 'Platos',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(max_length=10, unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=10, unique=True)),
                ('cantidad_persona', models.PositiveIntegerField(default=1, editable=False)),
                ('es_para_llevar', models.BooleanField(default=False, editable=False)),
                ('realizo_pedido', models.BooleanField(default=False, editable=False)),
                ('historial', models.OneToOneField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cliente', to='pedidos.historial')),
                ('mesa', models.OneToOneField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='pedidos.mesa')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_actual', models.DateTimeField(auto_now=True)),
                ('informacion', models.TextField(editable=False)),
                ('numero', models.PositiveIntegerField(editable=False, unique=True)),
                ('estado', models.CharField(choices=[('EN_PREPARACION', 'en_preparacion'), ('PAGADO', 'pagado'), ('PENDIENTE', 'pendiente'), ('PREPARADO', 'preparado'), ('SERVIDO', 'servido'), ('RESERVADO', 'reservado')], default=pedidos.models.Estado['pendiente'], max_length=50)),
                ('cliente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pedidos.cliente')),
                ('mesa', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pedidos.mesa')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
            },
        ),
        migrations.CreateModel(
            name='Mesero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(max_length=10, unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=10, unique=True)),
                ('identificacion', models.CharField(editable=False, max_length=7, null=True, unique=True)),
                ('esta_ocupado', models.BooleanField(default=False, editable=False)),
                ('pedidos', models.ManyToManyField(blank=True, editable=False, to='pedidos.pedido')),
            ],
            options={
                'verbose_name': 'Mesero',
                'verbose_name_plural': 'Meseros',
            },
        ),
        migrations.AddField(
            model_name='historial',
            name='pedidos',
            field=models.ManyToManyField(to='pedidos.pedido'),
        ),
        migrations.CreateModel(
            name='PersonalCocina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(max_length=10, unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=10, unique=True)),
                ('identificacion', models.CharField(editable=False, max_length=7, null=True, unique=True)),
                ('esta_cocinando', models.BooleanField(default=False, editable=False)),
                ('pedidos', models.ManyToManyField(blank=True, editable=False, to='pedidos.pedido')),
            ],
            options={
                'verbose_name': 'Personal de Cocina',
                'verbose_name_plural': 'Personales de Cocina',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platos', models.ManyToManyField(to='pedidos.plato')),
            ],
            options={
                'verbose_name': 'Menu',
                'verbose_name_plural': 'Menus',
            },
        ),
        migrations.CreateModel(
            name='ItemPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('observacion', models.CharField(blank=True, default='Ninguna', max_length=100)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_pedido_list', to='pedidos.cliente')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_pedido_list', to='pedidos.pedido')),
                ('plato', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pedidos.plato')),
            ],
            options={
                'verbose_name': 'Item del Pedido',
                'verbose_name_plural': 'Items del Pedido',
            },
        ),
        migrations.CreateModel(
            name='RegistroHistorico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pedidos', models.ManyToManyField(blank=True, editable=False, to='pedidos.pedido')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('clientes', models.ManyToManyField(blank=True, to='pedidos.cliente')),
                ('menu', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pedidos.menu')),
                ('mesas', models.ManyToManyField(blank=True, to='pedidos.mesa')),
                ('meseros', models.ManyToManyField(blank=True, to='pedidos.mesero')),
                ('pedidos', models.ManyToManyField(blank=True, to='pedidos.pedido')),
                ('personal_cocina_list', models.ManyToManyField(blank=True, to='pedidos.personalcocina')),
                ('registro_historico', models.OneToOneField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='restaurante', to='pedidos.registrohistorico')),
            ],
            options={
                'verbose_name': 'Restaurante',
                'verbose_name_plural': 'Restaurantes',
            },
        ),
    ]
