from django.contrib import admin
from .models import Menu, Categoria, Producto

class CategoriaInline(admin.TabularInline):
    model = Categoria
    extra = 1
    fields = ('nombre',)

# Personalizacion de la administracion del modelo Menu
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado')
    list_filter = ('estado',)
    search_fields = ('nombre',)

    actions = ['activar_menus', 'desactivar_menus']
    inlines = [CategoriaInline]
    @admin.action(description='Activar menús seleccionados')
    def activar_menus(self, request, queryset):
        queryset.update(estado=True)


    @admin.action(description='Desactivar menús seleccionados')
    def desactivar_menus(self, request, queryset):
        queryset.update(estado=False)


# Personalización de la administración del modelo Categoria
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'menu')
    list_filter = ('menu',)
    search_fields = ('nombre',)


# Personalización de la administración del modelo Producto
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'precio', 'disponibilidad', 'categoria')
    list_filter = ('disponibilidad', 'categoria')
    search_fields = ('nombre', 'descripcion')

    actions = ['cambiar_a_disponible', 'cambiar_a_no_disponible']

    @admin.action(description='Marcar como disponible')
    def cambiar_a_disponible(self, request, queryset):
        queryset.update(disponibilidad=True)

    @admin.action(description='Marcar como no disponible')
    def cambiar_a_no_disponible(self, request, queryset):
        queryset.update(disponibilidad=False)

