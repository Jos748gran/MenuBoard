from django.contrib import admin
from .models import (
    Impuesto, Cliente, Producto, ItemPedido, Pedido,
    Promocion, Factura, ItemFactura, PagoTransferencia,
    PagoEfectivo, PagoTarjeta, HistorialDeFactura
)

class MontoTotalFilter(admin.SimpleListFilter):
    title = 'monto total'
    parameter_name = 'monto_total'

    def lookups(self, request, model_admin):
        return [
            ('<100', 'Menos de 100'),
            ('100-500', 'Entre 100 y 500'),
            ('500-1000', 'Entre 500 y 1000'),
            ('>1000', 'Más de 1000'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '<100':
            return queryset.filter(factura_total_lt=100)
        if self.value() == '100-500':
            return queryset.filter(factura_totalgte=100, facturatotal_lt=500)
        if self.value() == '500-1000':
            return queryset.filter(factura_totalgte=500, facturatotal_lt=1000)
        if self.value() == '>1000':
            return queryset.filter(factura_total_gte=1000)
        return queryset

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1
    readonly_fields = ('precio_unitario',)

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'subtotal', 'impuesto_total', 'descuento', 'total', 'fecha', 'pedido')
    search_fields = ('numero', 'pedido_numero', 'pedidocliente_nombre')
    list_filter = ('fecha', 'pedido')
    readonly_fields = ('subtotal', 'impuesto_total', 'descuento', 'total')

    def save_model(self, request, obj, form, change):
        obj.calcular_monto_total()
        super().save_model(request, obj, form, change)

@admin.register(HistorialDeFactura)
class HistorialDeFacturaAdmin(admin.ModelAdmin):
    list_display = ('factura', 'fecha', 'monto_total')
    search_fields = ('factura_numero', 'facturapedidoclientenombre', 'factura_total')
    list_filter = ('factura__fecha', MontoTotalFilter)

    def fecha(self, obj):
        return obj.factura.fecha
    fecha.admin_order_field = 'factura__fecha'

    def monto_total(self, obj):
        return obj.factura.total

@admin.register(ItemFactura)
class ItemFacturaAdmin(admin.ModelAdmin):
    list_display = ('factura', 'producto', 'cantidad', 'subtotal')
    search_fields = ('factura_numero', 'producto_nombre')
    list_filter = ('factura',)
    readonly_fields = ('subtotal',)

    def save_model(self, request, obj, form, change):
        obj.calcular_subtotal()
        super().save_model(request, obj, form, change)
"""
@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
    search_fields = ('producto_nombre', 'pedido_numero')
    list_filter = ('pedido',)
    readonly_fields = ('precio_unitario',)

    def save_model(self, request, obj, form, change):
        obj.precio_unitario = obj.producto.precio
        super().save_model(request, obj, form, change)
"""
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'descripcion')
    search_fields = ('nombre',)
    list_filter = ('impuestos',)

@admin.register(Impuesto)
class ImpuestoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'porcentaje', 'descripcion')
    search_fields = ('nombre',)
    list_filter = ('porcentaje',)

#@admin.register(Cliente)
#class ClienteAdmin(admin.ModelAdmin):
    #list_display = ('nombre', 'cedula', 'correo_electronico', 'direccion', 'telefono')
    #search_fields = ('nombre', 'cedula', 'correo_electronico')
   # list_filter = ('direccion',)


@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'porcentaje_descuento')
    search_fields = ('descripcion',)
    list_filter = ('porcentaje_descuento',)

@admin.register(PagoTransferencia)
class PagoTransferenciaAdmin(admin.ModelAdmin):
    list_display = ('numero_transferencia', 'banco_origen', 'monto_pagado', 'cuenta_por_cobrar')
    search_fields = ('numero_transferencia', 'banco_origen')
    list_filter = ('banco_origen',)

@admin.register(PagoEfectivo)
class PagoEfectivoAdmin(admin.ModelAdmin):
    list_display = ('monto_pagado', 'cuenta_por_cobrar', 'cambio')
    search_fields = ('monto_pagado',)

@admin.register(PagoTarjeta)
class PagoTarjetaAdmin(admin.ModelAdmin):
    list_display = ('numero_tarjeta', 'titular', 'vencimiento', 'monto_pagado', 'cuenta_por_cobrar')
    search_fields = ('numero_tarjeta', 'titular')
    list_filter = ('vencimiento',)