from django.contrib import admin

from .models import (
    Producto, Item_Factura, Factura, Mesa, Persona, Mesero, Reporte, Grafico, Estadistica
)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria', 'cantidad_vendida',)
    search_fields = ('nombre', 'precio','categoria','cantidad_vendida',)
    list_filter = ('nombre', 'precio','categoria','cantidad_vendida',)

@admin.register(Item_Factura)
class Item_FacturaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'subtotal',)
    search_fields = ('cantidad', 'subtotal',)
    list_filter = ('producto', 'cantidad', 'subtotal',)

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'fecha', 'subtotal', 'impuesto', 'descuento','total', 'mesero', 'mesa',)
    search_fields = ('numero', 'fecha',)
    list_filter = ('numero', 'fecha', )

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('codigo','cantidad_uso',)
    search_fields = ('codigo','cantidad_uso',)
    list_filter = ('codigo','cantidad_uso',)

@admin.register(Mesero)
class MeseroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cedula', 'pedidosAtendidos',)
    search_fields = ('nombre', 'cedula','pedidosAtendidos',)
    list_filter = ('nombre', 'cedula',)


@admin.register(Estadistica)
class EstadisticaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_inicio', 'fecha_fin', 'mejor_mesero', 'mesa_mas_usada', 'producto_mas_vendido',)
    search_fields = ('titulo', 'fecha_inicio', 'fecha_fin',)
    list_filter = ('titulo', 'fecha_inicio', 'fecha_fin',)

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_inicio', 'fecha_fin',)
    search_fields = ('titulo', 'fecha_inicio', 'fecha_fin',)
    list_filter = ('titulo', 'fecha_inicio', 'fecha_fin',)

@admin.register(Grafico)
class GraficoAdmin(admin.ModelAdmin):
    list_display = ('titulo',)
    search_fields = ('titulo',)
    list_filter = ('titulo',)