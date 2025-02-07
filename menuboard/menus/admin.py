from django.contrib import admin
from .models import Menu

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado')
    list_filter = ('estado',)
    search_fields = ('nombre',)

    @admin.action(description='Activar menús seleccionados')
    def activar_menus(self, request, queryset):
        queryset.update(estado=True)


    @admin.action(description='Desactivar menús seleccionados')
    def desactivar_menus(self, request, queryset):
        queryset.update(estado=False)

