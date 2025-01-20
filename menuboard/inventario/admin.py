from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    Insumo, Operacion, Historial, Alerta, ReporteConsumo, Inventario, Proveedor,
    Pedido, Categoria, Usuario, Producto, Persona, Administrador, ReporteBodega
)


# Configuración del modelo Insumo
@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = (
    'identificador', 'nombre', 'cantidadDisponible', 'unidadMedida', 'nivelReorden', 'ubicacion', 'precioUnitario')
    search_fields = ('nombre', 'identificador')
    list_filter = ('unidadMedida',)
    ordering = ('nombre',)


# Configuración del modelo Operacion
@admin.register(Operacion)
class OperacionAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'insumo', 'cantidad', 'fechaRegistro', 'observaciones')
    search_fields = ('insumo__nombre', 'observaciones', 'tipo')
    list_filter = ('tipo', 'fechaRegistro')
    ordering = ('-fechaRegistro',)


# Configuración del modelo Historial
@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    list_display = ('operacion', 'descripcion')
    search_fields = ('operacion_insumo_nombre', 'descripcion')
    ordering = ('-operacion__fechaRegistro',)


# Configuración del modelo Alerta
@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ('mensaje', 'fecha', 'tipo')
    list_filter = ('tipo', 'fecha')
    search_fields = ('mensaje',)


# Configuración para reportes de consumo
@admin.register(ReporteConsumo)
class ReporteConsumoAdmin(admin.ModelAdmin):
    list_display = ('periodoInicio', 'periodoFin', 'datos')
    search_fields = ('datos',)
    date_hierarchy = 'periodoInicio'
    ordering = ('-periodoInicio',)

    def generarReporte(self, request, queryset):
        """
        Acción personalizada para generar reportes de consumo desde la interfaz administrativa.
        """
        for reporte in queryset:
            reporte.generarReporte()  # Genera los datos del reporte
        self.message_user(request, "Se generaron los reportes seleccionados correctamente.")

    actions = ['generarReporte']  # Agrega una acción para generar reportes desde el panel


# Configuración del modelo Inventario
@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('almacenamiento',)
    search_fields = ('almacenamiento',)
    ordering = ('almacenamiento',)


# Configuración del modelo Proveedor
@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'direccion', 'contacto')
    search_fields = ('nombre', 'email', 'contacto')
    ordering = ('nombre',)


# Configuración del modelo Pedido
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fecha', 'estado')
    search_fields = ('cliente', 'estado')
    list_filter = ('estado', 'fecha')
    date_hierarchy = 'fecha'
    ordering = ('-fecha',)


# Configuración del modelo Categoria
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)


# Configuración del modelo Usuario
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rol', 'email')
    search_fields = ('nombre', 'email', 'rol')
    ordering = ('nombre',)


# Configuración del modelo Producto
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio')
    search_fields = ('nombre',)
    ordering = ('nombre',)


# Configuración del modelo Persona
@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'edad')
    search_fields = ('nombre', 'apellido',)
    ordering = ('apellido',)


# Configuración del modelo Administrador
@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('revision', 'control')
    search_fields = ('revision', 'control')
    ordering = ('revision',)


# Configuración del modelo ReporteBodega
@admin.register(ReporteBodega)
class ReporteBodegaAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'datos')
    search_fields = ('tipo', 'datos')
    ordering = ('tipo',)