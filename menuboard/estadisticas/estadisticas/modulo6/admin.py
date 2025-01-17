from django.contrib import admin

from .models import (
    Producto, Item_Factura, Factura, Mesa, Persona, Mesero,estadistica_mesero, estadistica_mesa, estadistica_producto, Reporte, Grafico
)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria',)
    search_fields = ('nombre', 'precio','categoria',)
    list_filter = ('nombre', 'precio','categoria',)

@admin.register(Item_Factura)
class Item_FacturaAdmin(admin.ModelAdmin):
    list_display = ('cantidad',)
    search_fields = ('cantidad',)
    list_filter = ('cantidad',)

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'fecha', 'total', )
    search_fields = ('numero', 'fecha',)
    list_filter = ('numero', 'fecha', )

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('cantidad_uso', 'codigo', )
    search_fields = ('cantidad_uso', 'codigo',)
    list_filter = ('cantidad_uso', 'codigo',)

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cedula',)
    search_fields = ('nombre', 'cedula',)
    list_filter = ('nombre', 'cedula',)

@admin.register(Mesero)
class MeseroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cedula', 'pedidosAtendidos',)
    search_fields = ('nombre', 'cedula','pedidosAtendidos',)
    list_filter = ('nombre', 'cedula',)

@admin.register(estadistica_mesero)
class estadistica_meseroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'mejor_mesero',)
    search_fields = ('titulo', 'mejor_mesero',)
    list_filter = ('titulo', 'mejor_mesero',)

@admin.register(estadistica_mesa)
class estadistica_mesaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'mesa_mas_usada',)
    search_fields = ('titulo', 'mesa_mas_usada',)
    list_filter = ('titulo', 'mesa_mas_usada',)

@admin.register(estadistica_producto)
class estadistica_productoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'producto_mas_vendido',)
    search_fields = ('titulo', 'producto_mas_vendido',)
    list_filter = ('titulo', 'producto_mas_vendido',)

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('titulo',)
    search_fields = ('titulo',)
    list_filter = ('titulo',)

@admin.register(Grafico)
class GraficoAdmin(admin.ModelAdmin):
    list_display = ('titulo',)
    search_fields = ('titulo',)
    list_filter = ('titulo',)